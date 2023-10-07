# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import functools

from canonical import ResourceName

from .picqerresource import PicqerResource
from .product import Product
from .receiptproduct import ReceiptProduct
from .receiptpurchaseorder import ReceiptPurchaseOrder
from .receiptsupplier import ReceiptSupplier
from .userreference import UserReference


class Receipt(PicqerResource):
    idreceipt: int
    idwarehouse: int | None = None
    supplier: ReceiptSupplier | None = None
    purchaseorder: ReceiptPurchaseOrder | None = None
    receiptid: str
    status: str
    remarks: str | None = None
    completed_by: UserReference | None = None
    amount_received: int = 0
    amount_received_excessive: int = 0
    completed_at: datetime.datetime | None = None
    created: datetime.datetime
    products: list[ReceiptProduct] = []

    @property
    def resource_name(self) -> ResourceName:
        return ResourceName(f'//{self._client.domain}/receipts/{self.idreceipt}')

    @property
    def purchase_order_name(self) -> str | None:
        if not self.purchaseorder: return None
        return f'//{self._client.domain}/purchaseorders/{self.purchaseorder.idpurchaseorder}'

    def expects(self, product: int | str) -> bool:
        """Return a boolean indicting if this :class:`Receipt` expects the
        given product.
        
        Args:
            product: identifies the expected product. May be an :class:`int`
                (compare against :attr:`ReceiptProduct.idproduct`) or a
                :class:`str` (compare against :attr:`ReceiptProduct.productcode`).

        Returns:
            :class:`bool`
        """
        return self._expects(product)

    @functools.singledispatchmethod
    def _expects(self, product: int | str) -> bool:
        raise TypeError(type(product))

    @_expects.register
    def _expects_by_idproduct(self, product: int) -> bool:
        return any([x.idproduct == product for x in self.products])
    
    @_expects.register
    def _expects_by_sku(self, product: str) -> bool:
        return any([x.productcode == product for x in self.products])

    def is_completed(self) -> bool:
        return self.status == 'completed'

    async def receive(
        self,
        idproduct: int,
        amount: int = 1,
        idlocation: int | None = None
    ) -> ReceiptProduct:
        """Register the receipt of `amount` products of a single type
        specified by `idproduct`.
        """
        for i, product in enumerate(self.products):
            if product.idproduct != idproduct:
                continue
            response = await self._client.put(
                url=f'{self.get_persist_url()}/products/{product.idreceipt_product}',
                json={'delta': amount}
            )
            response.raise_for_status()
            product = self.products[i] = ReceiptProduct.parse_obj(await response.json())
            break
        else:
            if amount > 1:
                raise NotImplementedError
            response = await self._client.post(
                url=f'{self.get_persist_url()}/products',
                json={'idproduct': idproduct, 'force': True}
            )
            response.raise_for_status()
            product = ReceiptProduct.parse_obj(await response.json())
            self.products.append(product)
        if idlocation is not None:
            # Prior to updating the receipt, we must ensure that the Product
            # has the given location.
            spec = await self._client.retrieve(Product, product.idproduct)
            await spec.link_location(idlocation)
            response = await self._client.put(
                url=f'{self.get_persist_url()}/products/{product.idreceipt_product}',
                json={'stock_idlocation': idlocation}
            )
            response.raise_for_status()

        return product

    async def complete(self) -> None:
        """Mark the :class:`Receipt` as completed."""
        response = await self._client.put(
            url=self.get_persist_url(),
            json={"status": "completed"}
        )
        response.raise_for_status()

    async def mark_all_received(self) -> None:
        """Mark all products in the :class:`Receipt` as received for the amount
        expected.
        """
        response = await self._client.post(
            url=f'{self.get_persist_url()}/mark-all-received'
        )
        response.raise_for_status()

    def get_persist_url(self) -> str:
        return self.get_retrieve_url(self.idreceipt)

    class Meta:
        base_endpoint: str = '/v1/receipts'