# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic


class VIESResult(pydantic.BaseModel):
    id: str | None = pydantic.Field(
        default=None
    )

    country: str | None = pydantic.Field(
        default=None,
        alias='countryCode'
    )

    number: str | None = pydantic.Field(
        default=None,
        alias='vatNumber'
    )

    valid: bool = pydantic.Field(
        default=False
    )

    company: str | None = pydantic.Field(
        default=None,
        alias='traderName'
    )

    address: str | None = pydantic.Field(
        default=None,
        alias='traderAddress'
    )

    date: str | None = pydantic.Field(
        default=None
    )

    source: str = pydantic.Field(
        default="http://ec.europa.eu"
    )

    @pydantic.validator('valid') # type: ignore
    def preprocess_valid(cls, value: bool | str) -> bool:
        if isinstance(value, str):
            value = value == 'true'
        return value

    def is_valid(self) -> bool:
        return self.valid