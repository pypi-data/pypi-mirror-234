# Copyright (C) 2023 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic


class OrderPaymentDetails(pydantic.BaseModel):
    avs_result_code: str | None
    credit_card_bin: str | None
    credit_card_company: str | None
    credit_card_number: str | None
    cvv_result_code: str | None