# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime

from canonical import ResourceName

from headless.core import Reference
from .picqerresource import PicqerResource
from .purchaseorderproduct import PurchaseOrderProduct
from .receipt import Receipt
from .supplier import Supplier
from .user import User


class PurchaseOrder(PicqerResource):
    idpurchaseorder: int
    idsupplier: int | None = None
    idtemplate: int | None = None
    idwarehouse: int
    purchaseorderid: str | None = None
    supplier_name: str | None = None
    supplier_orderid: str | None = None
    status: str
    remarks: str | None = None
    delivery_date: datetime.date | None = None
    language: str | None = None
    idfulfilment_customer: int | None = None
    products: list[PurchaseOrderProduct] = []

    # TODO: These fields are not documented in the PurchaseOrder page, but are visible
    # in the Webhook documentation.
    completed_by_iduser: int | None = None
    completed_at: datetime.datetime | None = None

    # TODO: Is None when created through API, not documented.
    created_by_iduser: int | None = None
    created: datetime.datetime
    updated: datetime.datetime | None = None
    purchased_by_iduser: int | None = None
    purchased_at: datetime.datetime | None = None

    # Our fields
    supplier: Supplier = Reference(Supplier, 'idsupplier')

    @property
    def resource_name(self) -> ResourceName:
        return ResourceName(f'//{self._client.domain}/purchaseorders/{self.idpurchaseorder}')

    def get_product(self, idproduct: int) -> PurchaseOrderProduct:
        product: None | PurchaseOrderProduct = None
        for line in self.products:
            if line.idproduct != idproduct:
                continue
            product = line
            break
        else:
            raise KeyError(idproduct)
        return product

    def get_persist_url(self) -> str:
        return self.get_retrieve_url(self.idpurchaseorder)

    def is_purchased(self) -> bool:
        return self.status == 'purchased'

    def can_purchase(self) -> bool:
        return self.status == 'concept'

    async def create_receipt(self, remarks: str) -> Receipt:
        return await self._client.create(Receipt, {
            'idpurchaseorder': self.idpurchaseorder,
            'remarks': remarks
        })

    async def receipts(self, status: str | None = None) -> list[Receipt]:
        params: dict[str, str] = {'idpurchaseorder': str(self.idpurchaseorder)}
        if status:
            params['status'] = status
        return [
            receipt async for receipt in 
            self._client.listall(Receipt, params=params)
        ]

    async def get_purchaser(self) -> User | None:
        return await self._client.retrieve(User, self.purchased_by_iduser)\
            if self.purchased_by_iduser is not None\
            else None

    async def purchase(self) -> None:
        """Mark the :class:`PurchaseOrder` as ``purchased``."""
        if self.status != 'concept':
            raise ValueError("Only 'concept' purchase orders can be marked as purchased.")
        response = await self._client.post(
            url=f'{self.get_persist_url()}/mark-as-purchased'
        )
        response.raise_for_status()

    class Meta:
        base_endpoint: str = '/v1/purchaseorders'