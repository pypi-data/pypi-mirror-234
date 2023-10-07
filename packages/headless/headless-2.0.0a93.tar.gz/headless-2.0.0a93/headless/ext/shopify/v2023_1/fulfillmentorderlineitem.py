# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic


class FulfillmentOrderLineItem(pydantic.BaseModel):
    id: int
    shop_id: int
    fulfillment_order_id: int
    line_item_id: int
    inventory_item_id: int
    quantity: int
    fulfillable_quantity: int
    variant_id: int