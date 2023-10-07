# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import AsyncGenerator

from .base import WooCommerceResource
from .productvariationattribute import ProductVariationAttribute


class ProductVariation(WooCommerceResource):
    attributes: list[ProductVariationAttribute] = []
    id: int
    manage_stock: bool
    sku: str = ""

    class Meta:
        base_endpoint: str = '/products/{product_id}/variations'