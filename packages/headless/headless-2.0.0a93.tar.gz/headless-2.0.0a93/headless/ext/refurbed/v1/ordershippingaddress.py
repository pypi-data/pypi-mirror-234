# Copyright (C) 2023 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic


class OrderShippingAddress(pydantic.BaseModel):
    first_name: str
    family_name: str
    entity: str | None = None
    company_name: str | None = None
    company_vatin: str | None = None
    country_code: str
    post_code: str
    town: str
    street_name: str
    house_no: str
    supplement: str | None = None
    phone_number: str

    @property
    def display_name(self):
        return self.company_name if self.company_name else f'{self.first_name} {self.family_name}'