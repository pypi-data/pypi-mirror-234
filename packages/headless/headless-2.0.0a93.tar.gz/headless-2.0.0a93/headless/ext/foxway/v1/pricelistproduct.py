# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
import pydantic

from canonical import ResourceName
from headless.types import IResponse
from .base import FoxwayResource
from .dimension import Dimension


class PricelistProduct(FoxwayResource):
    dimension_group_id: int = pydantic.Field(
        default=...,
        alias='DimensionGroupId'
    )

    dimension_group_name: str = pydantic.Field(
        default=...,
        alias='DimensionGroupName'
    )

    item_variant_id: int = pydantic.Field(
        default=...,
        alias='ItemVariantId'
    )

    item_group_id: int = pydantic.Field(
        default=...,
        alias='ItemGroupId'
    )

    item_group_name: str = pydantic.Field(
        defailt=...,
        alias='ItemGroupName'
    )

    product_name: str = pydantic.Field(
        default=...,
        alias='ProductName'
    )

    sku: str = pydantic.Field(
        default=...,
        alias='SKU'
    )

    quantity: int = pydantic.Field(
        default=...,
        alias='Quantity'
    )

    price: float = pydantic.Field(
        default=...,
        alias='Price'
    )

    currency: str = pydantic.Field(
        default=...,
        alias='CurrencyIsoCode'
    )

    dimension: list[Dimension] = pydantic.Field(
        default=[],
        alias='Dimension'
    )

    @classmethod
    def get_list_url(cls, catalog_name: str) -> str: # type: ignore
        return cls._meta.base_endpoint.format(slug=catalog_name)

    @classmethod
    def get_next_url(cls, response: IResponse[Any, Any], n: int) -> str | None:
        return None

    @property
    def resource_name(self) -> ResourceName:
        return ResourceName(f'//foxway.shop/sku/{self.sku}')

    class Meta:
        base_endpoint: str = '/catalogs/{slug}/pricelist'