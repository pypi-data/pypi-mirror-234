# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import decimal
from datetime import datetime
from datetime import timezone

import pydantic

from .baseresource import BaseResource
from .harmonizedsystemcode import HarmonizedSystemCode


class InventoryItem(BaseResource):
    cost: decimal.Decimal
    country_code_of_origin: str
    country_harmonized_system_codes: list[HarmonizedSystemCode]
    created_at: datetime
    harmonized_system_code: int
    id: int
    province_code_of_origin: str
    sku: str
    tracked: bool
    updated_at: datetime
    requires_shipping: bool

    class Meta:
        base_endpoint: str = '/2023-01/inventory_items'
        name: str = 'inventory_item'
        persist_method: str = 'POST'
        pluralname: str = 'inventory_levels'