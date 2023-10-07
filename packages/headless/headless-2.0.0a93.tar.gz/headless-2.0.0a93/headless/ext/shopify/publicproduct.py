# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import decimal
from typing import Any

import pydantic

from .resource import ShopifyResource



class ProductVariantOptions(pydantic.BaseModel):
    option1: str | None = None
    option2: str | None = None


class PublicProductVariant(pydantic.BaseModel):
    title: str
    price: decimal.Decimal
    sku: str | None
    option1: str | None = None
    option2: str | None = None


class PublicProduct(ShopifyResource):
    id: int
    title: str
    variants: list[PublicProductVariant]

    class Meta:
        base_endpoint: str = '/products'
        pluralname: str = 'products'