# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Protocol

from .bearertokencredential import BearerTokenCredential


class ITokenResponse(Protocol):
    __module__: str = 'headless.ext.oauth2.types'
    access_token: BearerTokenCredential
    expires_in: int
    refresh_token: str | None