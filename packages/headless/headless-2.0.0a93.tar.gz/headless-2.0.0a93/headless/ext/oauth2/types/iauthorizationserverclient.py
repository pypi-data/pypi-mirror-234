# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Protocol

from .itokenresponse import ITokenResponse


class IAuthorizationServerClient(Protocol):
    __module__: str = 'headless.ext.oauth2.types'

    def get_issuer(self) -> str: ...
    def get_client_id(self) -> str: ...
    def get_token_endpoint(self) -> str: ...

    async def refresh_token(
        self,
        token: str,
        resource: str | None = None,
        scope: set[str] | None = None
    ) -> ITokenResponse:
        ...