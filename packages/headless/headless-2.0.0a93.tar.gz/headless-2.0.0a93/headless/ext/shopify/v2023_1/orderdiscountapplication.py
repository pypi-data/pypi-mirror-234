# Copyright (C) 2023 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import decimal
from typing import Literal

import pydantic


class OrderDiscountApplication(pydantic.BaseModel):
    allocation_method: Literal['across', 'each', 'one']
    code: str | None = None
    description: str | None = None
    target_selection: Literal['all', 'entitled', 'explicit']
    target_type: Literal['line_item', 'shipping_line']
    title: str | None = None
    type: Literal['automatic', 'discount_code', 'manual', 'script']
    value: decimal.Decimal
    value_type: Literal['fixed_amount', 'percentage']