# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic


class ReceiptProduct(pydantic.BaseModel):
    idreceipt_product: int
    idpurchaseorder_product: int
    idproduct: int
    idpurchaseorder: int
    productcode: str
    name: str
    amount: int
    amount_ordered: int
    amount_previously_received: int = 0
    added_by_receipt: bool = False

    # TODO: Shown in API examples but not in resource schema doc.
    abc_classification: str | None = None
    amount_receiving: int = 0
    amount_more_than_ordered: int = 0 
    amount_backorders: int = 0
    barcode: str | None = None
    stock: int = 0
    productcode_supplier: str | None = None
