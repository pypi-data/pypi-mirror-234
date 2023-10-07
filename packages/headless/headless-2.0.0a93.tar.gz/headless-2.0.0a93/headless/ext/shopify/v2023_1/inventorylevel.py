# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from datetime import timezone
from typing import Any

import pydantic
from canonical import ResourceName

from headless.types import IClient
from ..resource import ShopifyResource


class InventoryLevel(ShopifyResource):
    available: int
    inventory_item_id: int
    location_id: int
    disconnect_if_necessary: bool = False
    updated_at: datetime = pydantic.Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @property
    def resource_name(self) -> ResourceName:
        return ResourceName(
            f'//{self._client.domain}/inventoryitems/{self.inventory_item_id}/levels/{self.location_id}'
        )

    @classmethod
    async def connect(
        cls,
        client: IClient[Any, Any],
        location_id: int,
        inventory_item_id: int
    ) -> 'InventoryLevel':
        response = await client.post(
            url=f'{cls._meta.base_endpoint}/connect.json',
            json={
                'location_id': location_id,
                'inventory_item_id': inventory_item_id
            }
        )
        response.raise_for_status()
        dto = await response.json()
        resource = cls.parse_obj(dto['inventory_level'])
        resource._client = client
        return resource

    @classmethod
    def get_create_url(cls, *params: Any) -> str:
        return f'{cls._meta.base_endpoint}/set.json'

    def get_persist_url(self) -> str:
        return self.get_create_url()

    class Meta:
        base_endpoint: str = '/2023-01/inventory_levels'
        name: str = 'inventory_level'
        persist_method: str = 'POST'
        pluralname: str = 'inventory_levels'