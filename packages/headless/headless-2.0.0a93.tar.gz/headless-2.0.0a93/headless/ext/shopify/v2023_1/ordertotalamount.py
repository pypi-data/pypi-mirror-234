# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from decimal import Decimal

import pydantic


class OrderDisplayAmount(pydantic.BaseModel):
    amount: Decimal
    currency_code: str


class OrderTotalAmount(pydantic.BaseModel):
    shop_money: OrderDisplayAmount
    presentment_money: OrderDisplayAmount