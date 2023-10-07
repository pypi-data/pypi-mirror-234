# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import AsyncIterable

from .base import WooCommerceResource
from .productvariation import ProductVariation


class Product(WooCommerceResource):
    id: int
    manage_stock: bool
    name: str
    sku: str = ""
    variations: list[int] = []

    async def variants(self) -> AsyncIterable[ProductVariation]:
        url = self.get_retrieve_url(self.id) + '/variations'
        async for variation in self._client.listall(ProductVariation, url=url):
            yield variation

    class Meta:
        base_endpoint: str = '/products'