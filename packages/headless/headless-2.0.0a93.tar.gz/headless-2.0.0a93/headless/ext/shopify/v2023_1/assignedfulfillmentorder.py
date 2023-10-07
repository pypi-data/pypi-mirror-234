# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Callable
from typing import TypeVar

from canonical import ResourceName

from .baseresource import BaseResource
from .fulfillmentorder import FulfillmentOrder
from .fulfillmentorderdestination import FulfillmentOrderDestination
from .fulfillmentorderlineitem import FulfillmentOrderLineItem


D = TypeVar('D')


class AssignedFulfillmentOrder(BaseResource):
    assigned_location_id: int
    destination: dict[str, Any] | None
    id: int
    line_items: list[FulfillmentOrderLineItem] = []
    order_id: int
    request_status: str
    shop_id: int
    status: str

    @classmethod
    def process_response(
        cls,
        action: str,
        data: dict[str, Any]
    ) -> dict[str, Any]:
        if action not in {'list', None}:
            # Only listing is supported.
            raise NotImplementedError(action)
        return data['fulfillment_orders'] if action else data

    @property
    def resource_name(self) -> ResourceName:
        return f'//{self._client.domain}/fulfillment_orders/{self.id}'

    @property
    def order_name(self) -> ResourceName:
        return ResourceName(f'//{self._client.domain}/orders/{self.order_id}')

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

    async def get_fulfillment_order(self) -> FulfillmentOrder:
        return await self._client.retrieve(FulfillmentOrder, self.id)

    class Meta:
        base_endpoint: str = '/2023-01/assigned_fulfillment_orders'