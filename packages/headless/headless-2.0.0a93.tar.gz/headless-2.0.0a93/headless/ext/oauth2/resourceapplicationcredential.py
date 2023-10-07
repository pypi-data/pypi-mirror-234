# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
import urllib.parse
from typing import Any

from headless.core import BaseCredential
from headless.types import IClient
from headless.types import IRequest
from headless.types import IResponse
from headless.types import WWWAuthenticateHeader
from .client import Client
from .models import AccessToken
from .models import AccessTokenKey
from .nullclientstorage import NullClientStorage
from .types import IClientStorage


class ResourceApplicationCredential(BaseCredential):
    """A :class:`~headless.core.BaseCredential` implementation that uses
    a :class:`~headless.ext.oauth2.ApplicationClient` instance to retrieve
    an access token for a resource using the ``client_credentials`` grant.
    """
    __module__: str = 'headless.ext.oauth2'
    access_tokens: dict[str, AccessToken] = {}
    client: Client
    storage: IClientStorage

    @property
    def client_id(self) -> str:
        assert self.client.client_id is not None
        return self.client.client_id

    def __init__(
        self,
        client: Client,
        storage: IClientStorage = NullClientStorage()
    ):
        self.client = client
        self.storage = storage

    async def add_to_request(self, request: IRequest[Any]) -> None:
        request.add_header('Authorization', f'Bearer {await self.get_token(request)}')

    async def get_token(
        self,
        request: IRequest[Any],
        scope: set[str] | None = None,
        force: bool = False
    ) -> str:
        p = urllib.parse.urlparse(request.url)
        resource = f'{p.scheme}://{p.netloc}'
        access_token = self.access_tokens.get(resource)\
            or await self.storage.get(AccessTokenKey(self.client_id, resource))
        if access_token is None or force:
            scope = scope or set()
            if access_token is not None:
                scope.update(access_token.scope)
            async with self.client:
                response = await self.client.client_credentials(
                    scope=scope or set(),
                    resource=resource
                )
            self.access_tokens[resource] = access_token = AccessToken.from_response(
                client_id=self.client_id,
                resource=resource,
                scope=scope,
                token=response.access_token,
                ttl=response.expires_in
            )
        return access_token.get_access_token()

    async def refresh(self, request: IRequest[Any], scope: set[str]) -> None:
        await self.get_token(request, scope=scope, force=True)

    async def process_response(
        self,
        client: IClient[Any, Any],
        request: IRequest[Any],
        response: IResponse[Any, Any]
    ) -> IResponse[Any, Any]:
        if request.is_retry():
            return response
        if response.status_code in {401, 403}\
        and response.headers.get('www-authenticate'):
            header = WWWAuthenticateHeader.parse(response.headers['www-authenticate'])
            scope = set(filter(bool, re.split(r'\s+', header.get('scope') or '')))
            if header.get('error') == 'insufficient_scope' and request.tag('oauth2:obtain'):
                # The access token needs additional scope to be accepted by the
                # resource server.
                await self.refresh(request, scope)
                response = await client.send_request(request, self)
            if header.get('error') == 'invalid_token' and request.tag('oauth2:refresh'):
                # Token might be expired, but retry this only once because we might
                # end up in an infite loop if the token was rejected for any other
                # reason.
                await self.refresh(request, scope)
                response = await client.send_request(request, self)
        return response