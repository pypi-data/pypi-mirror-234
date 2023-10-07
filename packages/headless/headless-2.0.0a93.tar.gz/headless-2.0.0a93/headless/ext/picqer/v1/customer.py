# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic
from canonical import EmailAddress
from canonical import ResourceName

from .picqerresource import PicqerResource


class Customer(PicqerResource):
    idcustomer: int
    contactname: str | None
    emailaddress: EmailAddress | None
    name: str

    @pydantic.validator('emailaddress', pre=True) # type: ignore
    def preprocess_emailaddress(cls, value: str | None) -> str | None:
        return value or None

    @property
    def resource_name(self) -> ResourceName:
        return ResourceName(f'//{self._client.domain}/customers/{self.idcustomer}')

    def is_company(self) -> bool:
        return self.contactname is not None

    class Meta:
        base_endpoint: str = '/v1/customers'