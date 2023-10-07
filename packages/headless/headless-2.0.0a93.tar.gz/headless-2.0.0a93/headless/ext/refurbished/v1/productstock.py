# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal

from .versionresource import VersionResource


class ProductStock(VersionResource):
    product_id: int
    product_title: str
    condition: Literal['refurbished', 'new']
    grade: Literal['A', 'B', 'C']
    ex_purchase_price: float
    ex_retail_price: float
    margin: bool
    stock: int

    class Meta:
        base_endpoint: str = '/v1/product/stock'