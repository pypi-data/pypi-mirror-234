# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic


class FulfillmentOrderDestination(pydantic.BaseModel):
    address1: str
    address2: str | None
    city: str
    company: str | None
    country: str
    id: int
    email: str | None
    first_name: str
    last_name: str
    phone: str | None
    province: str | None
    zip: str
