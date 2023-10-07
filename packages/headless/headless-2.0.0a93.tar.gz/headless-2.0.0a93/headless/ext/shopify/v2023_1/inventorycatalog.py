# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Iterator

from headless.core import BaseInventoryCatalog
from .product import Product
from .productvariant import ProductVariant


class InventoryCatalog(BaseInventoryCatalog[Product]):
    __module__: str = 'headless.ext.shopify.v2023_1'
    model = Product
    _products: dict[int, Product]
    _sku_index: dict[str, ProductVariant]

    def __init__(self) -> None:
        self._products = {}
        self._sku_index = {}

    def add(self, obj: Product) -> None:
        self._products[obj.id] = obj
        for variant in obj.variants:
            if not variant.sku:
                continue
            self._sku_index[variant.sku] = variant

    def count(self) -> int:
        return len(self._sku_index)

    def get_by_sku(self, sku: str) -> tuple[Product | None, ProductVariant | None]:
        if sku not in self._sku_index: return (None, None)
        variant = self._sku_index[sku]
        return self._products[variant.product_id], variant

    def __iter__(self) -> Iterator[tuple[Product, ProductVariant]]:
        for variant in self._sku_index.values():
            yield self._products[variant.product_id], variant