# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import Any
from typing import Callable
from typing import Literal
from typing import TypeVar

from canonical import ResourceName

from .baseresource import BaseResource
from .fulfillmentorderdestination import FulfillmentOrderDestination
from .fulfillmentorderlineitem import FulfillmentOrderLineItem
from .order import Order


D = TypeVar('D')


class FulfillmentOrder(BaseResource):
    assigned_location_id: int
    # assigned_location
    created_at: datetime.datetime
    destination: dict[str, Any] | None
    # delivery_method
    fulfill_at: datetime.date | str | None
    fulfill_by: datetime.date | str | None
    # fulfillment_holds
    id: int
    # international_duties
    line_items: list[FulfillmentOrderLineItem]
    order_id: int
    request_status: Literal['unsubmitted', 'submitted', 'accepted', 'rejected', 'cancellation_requested', 'cancellation_accepted', 'cancellation_rejected', 'closed']
    shop_id: int
    status: Literal['open', 'in_progress', 'scheduled', 'cancelled', 'on_hold', 'incomplete', 'closed']
    supported_actions: list[str]
    # merchant_requests
    updated_at: datetime.datetime

    @property
    def resource_name(self) -> ResourceName:
        return f'//{self._client.domain}/fulfillment_orders/{self.id}'

    def get_destination(self, parse: Callable[..., D] = FulfillmentOrderDestination) -> D:
        return parse(self.destination)

    def has_destination(self) -> bool:
        return self.destination is not None

    async def reject(self) -> None:
        response = await self._client.post(
            url=f'2023-01/fulfillment_orders/{self.id}/fulfillment_request/reject.json',
            json={}
        )
        response.raise_for_status()

    async def get_order(self) -> Order:
        return await self._client.retrieve(Order, self.order_id)

    class Meta:
        base_endpoint: str = '/2023-01/fulfillment_orders'