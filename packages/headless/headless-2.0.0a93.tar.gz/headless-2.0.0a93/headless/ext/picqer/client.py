# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from headless.core import httpx
from headless.core import LinearBackoff
from headless.types import IBackoff
from .credential import PicqerCredential

from . import v1


class Client(httpx.Client):
    backoff: IBackoff = LinearBackoff(5, 15)

    def __init__(
        self,
        api_url: str,
        api_email: str,
        api_key: str,
    ):
        super().__init__(
            base_url=api_url,
            credential=PicqerCredential(api_email, api_key)
        )

    async def get_product_by_sku(self, sku: str) -> v1.Product | None:
        """Lookup a product by its SKU."""
        result = None
        async for product in self.listall(v1.Product, params={'productcode': sku}):
            assert product.productcode == sku
            result = product
        return result
