# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime

from canonical import ResourceName

from .picqerresource import PicqerResource


class StockHistory(PicqerResource):
    idproduct_stock_history: int
    idproduct: int
    idwarehouse: int
    iduser: int | None
    old_stock: int
    stock_change: int
    new_stock: int
    reason: str
    change_type: str
    changed_at: datetime.datetime

    @property
    def resource_name(self) -> ResourceName:
        return ResourceName(f'//{self._client.domain}/stockhistory/{self.idproduct_stock_history}')

    class Meta:
        base_endpoint: str = '/v1/stockhistory'