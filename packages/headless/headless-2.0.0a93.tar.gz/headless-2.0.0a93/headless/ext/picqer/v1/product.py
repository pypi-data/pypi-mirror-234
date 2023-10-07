# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from canonical import ResourceName

from .picqerresource import PicqerResource
from .productfield import ProductField
from .productpricelist import ProductPricelist
from .productstock import ProductStock
from .tag import Tag


class Product(PicqerResource):
    idproduct: int
    idvatgroup: int
    name: str
    price: float
    fixedstockprice: float | None = None
    idsupplier: int | None = None
    productcode: str
    productcode_supplier: str | None = None
    deliverytime: int | None = None
    description: str | None = None
    barcode: str | None = None
    type: str | None = None
    unlimitedstock: bool = False
    weight: int | None = None
    length: int | None = None
    width: int | None = None
    height: int | None = None
    minimum_purchase_quantity: int | None = None
    purchase_in_quantities_of: int | None = None
    hs_code: str | None = None
    country_of_origin: str | None = None
    active: bool = True
    idfulfilment_customer: int | None = None
    analysis_pick_amount_per_day: float | None = None
    pricelists: list[ProductPricelist] = []

    # Not documented but present in response and Picqer examples.
    productfields: list[ProductField] = []
    images: list[str] = []
    stock: list[ProductStock] = []
    tags: dict[str, Tag] = {}

    @property
    def resource_name(self) -> ResourceName:
        return self.get_resource_name(self._client.domain)

    def get_resource_name(self, domain: str | None = None) -> ResourceName:
        return ResourceName(f'//{domain}/products/{self.idproduct}')

    def get_persist_url(self, path: str = '') -> str:
        url = self.get_retrieve_url(self.idproduct)
        if path:
            if path.startswith('/'):
                raise ValueError(path)
        return str.join('/', [url, path]) if path else url

    def get_field(self, idproductfield: int | str) -> Any | None:
        return self.get_product_field(idproductfield)

    def get_product_field(self, idproductfield: int | str) -> Any | None:
        for field in self.productfields:
            if isinstance(idproductfield, int) and field.idproductfield == idproductfield:
                value = field.value
                break
            elif isinstance(idproductfield, str) and field.title == idproductfield:
                value = field.value
                break
        else:
            value = None
        return value
    
    def get_total_free_stock(self, idwarehouse: int | None = None) -> int:
        stock: int = 0
        for warehouse in self.stock:
            if idwarehouse is not None and warehouse.idwarehouse != idwarehouse:
                continue
            stock += warehouse.freestock
        return stock

    def has_tag(self, name: int) -> bool:
        return any([x.idtag == name for x in self.tags.values()])

    async def link_location(self, idlocation: int) -> None:
        """Links the specified location to this :class:`Product`."""
        response = await self._client.post(
            url=f'{self.get_persist_url()}/locations',
            json={'idlocation': idlocation}
        )
        response.raise_for_status()

    async def set_field(self, idproductfield: int, value: Any) -> None:
        include: set[str] = {'idproductfield', 'value'}
        changed_field: dict[str, Any]
        for field in self.productfields:
            if field.idproductfield != idproductfield:
                continue
            field.value = value
            changed_field = field.dict(include=include)
        else:
            changed_field = {'idproductfield': idproductfield, 'value': value}
        fields = [
            x.dict(include=include)
            for x in self.productfields if x.idproductfield != idproductfield
        ]
        fields.append(changed_field)
        response = await self._client.put(
            url=self.get_persist_url(),
            json={'productfields': fields}
        )
        response.raise_for_status()

    async def tag(self, idtag: int) -> None:
        response = await self._client.post(
            url=self.get_persist_url(path='tags'),
            json={'idtag': idtag}
        )
        response.raise_for_status()

    class Meta:
        base_endpoint: str = '/v1/products'