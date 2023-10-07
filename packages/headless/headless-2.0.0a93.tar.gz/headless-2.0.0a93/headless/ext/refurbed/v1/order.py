# Copyright (C) 2023 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import decimal
import datetime

import pydantic

from .orderitem import OrderItem
from .ordershippingaddress import OrderShippingAddress


class Order(pydantic.BaseModel):
    customer_email: str | None = None
    has_invoice: bool
    id: int
    items: list[OrderItem] = []
    released_at: datetime.datetime
    shipping_address: OrderShippingAddress
    total_charged: decimal.Decimal