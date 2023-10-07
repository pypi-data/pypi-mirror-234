# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from headless.ext.oauth2.models import ServerMetadata
from headless.types import IClient
from headless.types import IRequest
from headless.types import IResponse


class Server:
    """Provides an interface to an OAuth 2.x/OpenID Connect authorization
    server. May be autodiscovered using the Metadata Endpoint, or manually
    configured. When configuring manually, at least the `token_endpoint`
    parameter must be provided.
    """
    __module__: str = 'headless.ext.oidc'

    def __init__(
        self,
        issuer: str,
        autodiscover: bool = True,
        token_endpoint: str | None = None,
        metadata_endpoint: str | None = None
    ) -> None:
        self.autodiscover = autodiscover and not bool(token_endpoint)
        self.issuer = issuer
        self.metadata = ServerMetadata(issuer=issuer)
        self.metadata_endpoint = metadata_endpoint

    async def discover(self, client: IClient[IRequest[Any], IResponse[Any, Any]]) -> None:
        raise NotImplementedError