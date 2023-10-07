# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import decimal
from datetime import datetime
from typing import Any

from canonical import EmailAddress
from canonical import Phonenumber

from headless.types import IClient
from .baseresource import BaseResource
from .customeraddress import CustomerAddress
from .customermetafield import CustomerMetafield
from .customeremailmarketingconsent import CustomerEmailMarketingConsent
from .customersmsmarketingconsent import CustomerSmsMarketingConsent
from .partialcustomeraddress import PartialCustomerAddress
from .metafield import Metafield
from .metafieldset import MetafieldSet


class Customer(BaseResource):
    accepts_marketing: bool = False
    accepts_marketing_updated_at: datetime
    addresses: list[CustomerAddress | PartialCustomerAddress] = []
    currency: str
    created_at: datetime
    default_address: CustomerAddress | PartialCustomerAddress | None = None
    email: EmailAddress | None = None
    email_marketing_consent: CustomerEmailMarketingConsent | None = None
    first_name: str | None
    id: int
    last_name: str | None
    last_order_id: int | None = None
    last_order_name: str | None = None
    metafields: list[CustomerMetafield] = []
    marketing_opt_in_level: str | None = None
    multipass_identifier: str | None = None
    name: str | None = None
    note: str | None = None
    orders_count: int = 0
    password: str | None = None
    password_confirmation: str | None = None
    phone: Phonenumber | None = None
    sms_marketing_consent: CustomerSmsMarketingConsent | None = None
    state: str  = 'enabled'
    tags: str
    tax_exempt: bool = False
    total_spent: decimal.Decimal | None = None
    updated_at: datetime
    verified_email: bool = False

    @classmethod
    def get_metafields_url(cls, resource_id: int) -> str:
        return f'{cls._meta.base_endpoint}/{resource_id}/metafields.json'

    def get_persist_url(self) -> str:
        return self.get_retrieve_url(self.id)

    def set_metafield(self, qualname: str, value: Any) -> None:
        namespace, key = str.split(qualname, '.')
        self.metafields.append(CustomerMetafield.parse_obj({
            'namespace': namespace,
            'key': key,
            'value': value
        }))

    async def persist(
        self,
        client: IClient[Any, Any] | None = None,
        include: set[str] | None = None,
        exclude: set[str] | None = None,
    ):
        include = include or set()
        include.add('id')
        if self.metafields:
            # Metafields need to be persisted separately.
            include.remove('metafields')
            metafields = self.metafields
            for field in metafields:
                self.metafields = []
                self.metafields.append(field)
                await super().persist(client, {'id', 'metafields'})
        if len(include) > 1:
            return await super().persist(client, include, exclude)

    async def get_metafields(self) -> MetafieldSet:
        """Return the metafields defined for this resource."""
        iterator = self._client.listall(
            Metafield,
            params={
                'metafield[owner_resource]': str.lower(type(self).__name__),
                'metafield[owner_id]': self.id
            }
        )
        return MetafieldSet(self._client, self, [x async for x in iterator])

    class Meta:
        base_endpoint: str = '/2023-01/customers'