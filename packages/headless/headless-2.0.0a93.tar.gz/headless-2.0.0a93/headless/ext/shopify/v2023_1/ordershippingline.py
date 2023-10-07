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


class OrderShippingLine(pydantic.BaseModel):
    code: str
    price: Decimal
    # TODO
    # price_set
    source: str
    title: str

    # TODO
    # tax_lines
    # carrier_identifier
    # requested_fulfillment_service_id