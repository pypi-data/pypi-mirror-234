# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from typing import Any

from headless.core import httpx
from .credential import RefurbedCredential
from .v1 import Order


class BaseClient(httpx.Client):
    __module__: str = 'headless.ext.refurbed'

    def __init__(self, access_token: str | None = None):
        access_token = access_token or os.environ['REFURBED_API_KEY']
        super().__init__(
            base_url='',
            credential=RefurbedCredential(access_token)
        )

    def get_base_url(self, base_url: str) -> str:
        raise NotImplementedError
    
    async def accept_order_item(self, item_id: int):
        response = await self.post(
            url='/refb.merchant.v1.OrderItemService/UpdateOrderItemState',
            json={
                'id': item_id,
                'state': 'ACCEPTED',
            }
        )
        response.raise_for_status()
    
    async def ship_order_item(self, item_id: int):
        response = await self.post(
            url='/refb.merchant.v1.OrderItemService/UpdateOrderItemState',
            json={
                'id': item_id,
                'state': 'SHIPPED',
            }
        )
        response.raise_for_status()

    async def get_order(self, order_id: str) -> Order:
        response = await self.post(
            url="/refb.merchant.v1.OrderService/GetOrder",
            json={"id": order_id}
        )
        response.raise_for_status()
        dto = await response.json()
        return Order.parse_obj(dto['order'])

    async def list_orders(self, state: str = "NEW") -> list[Order]:
        """List all orders, ordered by date."""
        response = await self.post(
            url="/refb.merchant.v1.OrderService/ListOrders",
            json={
                "pagination": {
                    "limit": 10
                },
                "sort": {
                    "order": "DESC",
                    "by": "ID"
                },
                "filter": {
                    "state": {"any_of": [state]}
                }
            }
        )
        response.raise_for_status()
        dto = await response.json()
        return [Order.parse_obj(x) for x in (dto.get('orders') or [])]

    async def update_offer(self, sku: str, **params: Any) -> None:
        """Updates an Offer."""
        response = await self.post(
            url="/refb.merchant.v1.OfferService/UpdateOffer",
            json={
                **params,
                'identifier': {
                    'sku': sku
                }
            }
        )
        response.raise_for_status()

    async def update_order_item(self, item_id: int | str, **params: Any) -> None:
        response = await self.post(
            url="/refb.merchant.v1.OrderItemService/UpdateOrderItem",
            json={
                **params,
                'id': str(item_id)
            }
        )
        response.raise_for_status()