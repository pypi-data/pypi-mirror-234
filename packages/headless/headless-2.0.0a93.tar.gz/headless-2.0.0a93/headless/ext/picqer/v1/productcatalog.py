# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from collections import OrderedDict
from typing import Any, Iterator

from headless.types import IClient
from headless.types import IProductCatalog
from .product import Product


class ProductCatalog(IProductCatalog[Product]):
    __module__: str = 'headless.ext.picqer.v1'
    model: type[Product] = Product
    _index_sku: dict[str, Product] = OrderedDict()
    _index_id: dict[int, Product] = OrderedDict()

    def __init__(self, client: IClient[Any, Any]) -> None:
        self.client = client

    def get_by_product_id(self, product_id: int | str) -> Product | None:
        assert isinstance(product_id, int)
        return self._index_id.get(product_id)

    def get_by_sku(self, sku: str) -> Product | None:
        return self._index_sku.get(sku)

    async def retrieve(self) -> None:
        self.logger.debug("Retrieving product catalog (domain: %s)", self.client.domain)
        async for dto in self.client.listall(self.model):
            self._index_id[dto.idproduct] = dto
            self._index_sku[dto.productcode] = dto
        self.logger.info(
            "Retrieved product catalog (domain: %s, products: %s)",
            self.client.domain, len(self._index_id)
        )

    def __iter__(self) -> Iterator[Product]:
        return 