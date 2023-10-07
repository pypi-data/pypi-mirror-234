# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Callable
from typing import Literal

import pydantic

from .bearertokencredential import BearerTokenCredential
from .encodedidtoken import EncodedIDToken


class TokenResponse(pydantic.BaseModel):
    token_type: Literal['Bearer', 'bearer']
    expires_in: int
    access_token: BearerTokenCredential
    refresh_token: str | None = None
    id_token: EncodedIDToken | None = None
    scope: str | None = None

    @pydantic.validator('access_token')
    def validate_access_token(
        cls,
        value: str | BearerTokenCredential | None
    ) -> BearerTokenCredential | None:
        if isinstance(value, str):
            value = BearerTokenCredential(value)
        return value
    
    class Config:
        json_encoders: dict[type[BearerTokenCredential], Callable[..., str]] = {
            BearerTokenCredential: BearerTokenCredential.__str__
        }