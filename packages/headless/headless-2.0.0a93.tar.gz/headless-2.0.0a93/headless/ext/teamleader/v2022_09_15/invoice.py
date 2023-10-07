# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import date
from datetime import datetime
from datetime import timezone
from typing import Any

from httpx import AsyncClient

from ..resource import TeamleaderResource
from .invoicecustomfield import InvoiceCustomField
from .invoicedparty import InvoiceParty


class Invoice(TeamleaderResource):
    custom_fields: list[InvoiceCustomField] = []
    id: str
    invoicee: InvoiceParty
    invoice_number: str | None = None
    invoice_date: date | None = None
    paid: bool
    paid_at: datetime | None
    status: str

    @classmethod
    def get_create_url(cls, *params: Any) -> str:
        return f'{cls._meta.base_endpoint}.draft'

    @classmethod
    def get_retrieve_url(cls, resource_id: int | str | None) -> str:
        return f'{cls._meta.base_endpoint}.info'

    def get_field(self, field_id: str) -> Any:
        for field in self.custom_fields:
            if field.definition.id != field_id:
                continue
            value = field.value
            break
        else:
            raise AttributeError(f"No such field: {field_id}")
        return value
    
    async def set_fields(self, data: dict[str, Any]):
        """Set the given fields to the given values."""
        # TODO: The list endpoint does not return all objects.
        obj = await self._client.retrieve(type(self), self.id)
        provided: set[str] = {x for x in data.keys()}
        self.custom_fields = obj.custom_fields
        fields = [
            {'id': field.definition.id, 'value': field.value}
            for field in self.custom_fields
            if field.definition.id not in provided
        ]
        for field_id, value in data.items():
            if isinstance(value, (datetime, date)):
                value = value.isoformat()
            fields.append({'id': field_id, 'value': value})
        await self._client.persist(type(self), self, data={
            'id': self.id,
            'custom_fields': fields
        })

    async def download(self, fmt: str = 'pdf') -> bytes:
        """Download the invoice and return a byte-sequence holding the data."""
        response = await self._client.post(
            url=f'{self._meta.base_endpoint}.download',
            params={'id': self.id, 'format': fmt}
        )
        response.raise_for_status()
        dto = await response.json()
        async with AsyncClient() as client:
            response = await client.get(url=dto['data']['location'])
            response.raise_for_status()
        return response.content

    async def issue(self, invoice_date: date | None = None) -> None:
        response = await self._client.post(url='/invoices.book', json={
            'id': self.id,
            'on': (invoice_date or date.today()).isoformat()
        })
        response.raise_for_status()

    async def register_payment(
        self,
        amount: float,
        currency: str,
        paid_at: datetime | None = None
    ) -> None:
        response = await self._client.post(
            url='/invoices.registerPayment',
            json=  {
                "id": self.id,
                "payment": {
                "amount": amount,
                "currency": currency
                },
                "paid_at": (paid_at or datetime.now(tz=timezone.utc)).isoformat(timespec="seconds", sep='T')
            }
        )
        response.raise_for_status()

    class Meta(TeamleaderResource.Meta):
        base_endpoint: str = '/invoices'