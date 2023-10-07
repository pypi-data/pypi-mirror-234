# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic


class PartialCustomerAddress(pydantic.BaseModel):
    address1: str | None
    address2: str | None
    city: str | None
    company: str | None
    country: str | None
    country_code: str | None
    default: bool = False
    first_name: str 
    last_name: str
    latitude: float | None = None
    longitude: float | None = None
    name: str
    phone: str | None
    province: str | None
    province_code: str | None
    zip: str | None

    def is_partial(self) -> bool:
        return True