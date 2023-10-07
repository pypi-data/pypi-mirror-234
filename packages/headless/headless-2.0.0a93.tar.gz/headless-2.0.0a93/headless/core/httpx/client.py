# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import copy
import ssl
from typing import Any
from typing import TypeVar

import certifi
import httpx

from headless.types import ConnectTimeout
from headless.types import IClient
from headless.types import ICredential
from headless.types import IRequest
from headless.types import IResponseCache
from headless.types import NullCredential
from headless.types import ReadTimeout
from headless.types import RequestContent
from ..cachekeybuilder import CacheKeyBuilder
from ..nullresponsecache import NullResponseCache
from ..resource import Resource # type: ignore
from .request import Request
from .response import Response


R = TypeVar('R', bound=Resource)
T = TypeVar('T', bound='Client')


class Client(IClient[httpx.Request, httpx.Response]):
    _client: httpx.AsyncClient
    cache_key_factory: CacheKeyBuilder = CacheKeyBuilder()
    client_kwargs: dict[str, Any]
    response_class: type[Response] = Response
    request_class: type[Request] = Request

    @property
    def cookies(self) -> Any:
        return self._client.cookies

    def __init__(
            self,
            *,
            base_url: str,
            credential: ICredential = NullCredential(),
            cache: IResponseCache = NullResponseCache(),
            app: Any | None = None,
            **kwargs: Any
        ):
        super().__init__(base_url=base_url, credential=credential)
        self.app = app
        self.cache = cache
        self.ssl = ssl.create_default_context()
        self.ssl.load_verify_locations(certifi.where())
        self.client_kwargs = copy.deepcopy(kwargs)
        self._client = httpx.AsyncClient(
            app=app,
            base_url=self.base_url,
            verify=self.ssl,
            **kwargs
        )
        self._in_context = False

    def cache_key(self, *args: Any, **kwargs: Any) -> str:
        return self.cache_key_factory.build(*args, **kwargs)
    
    async def from_cache(self, *args: Any, **kwargs: Any) -> tuple[str, Any]:
        key = self.cache_key(*args, **kwargs)
        return key, await self.cache.get(key)
    
    async def to_cache(self, key: str, data: str) -> None:
        await self.cache.set(key, data)

    def in_context(self) -> bool:
        return self._in_context

    async def request_factory(
        self,
        method: str,
        url: str,
        json: list[Any] | dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        cookies: dict[str, str] | None = None,
        content: RequestContent | None = None,
        data: dict[str, str] | None = None
    ) -> httpx.Request:
        return self._client.build_request(
            method=method,
            url=url,
            json=json,
            headers=headers,
            params=params,
            cookies=cookies,
            content=content,
            data=data
        )

    async def send(self, request: IRequest[Any]) -> Response: # type: ignore
        try:
            return Response.fromimpl(request, await self._client.send(request.impl))
        except httpx.ConnectTimeout:
            raise ConnectTimeout(self, request)
        except httpx.ReadTimeout:
            raise ReadTimeout(self, request)

    async def __aenter__(self: T) -> T:
        if not self.in_context():
            await self._client.__aenter__()
            self._in_context = True
        return self

    async def __aexit__(self, cls: type[BaseException] | None, *args: Any) -> bool | None:
        if self.in_context():
            self._in_context = False
            await self._client.__aexit__(cls, *args)
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                verify=self.ssl,
                app=self.app,
                **self.client_kwargs
            )