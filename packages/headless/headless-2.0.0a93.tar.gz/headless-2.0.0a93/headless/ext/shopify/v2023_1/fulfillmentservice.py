# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .baseresource import BaseResource


class FulfillmentService(BaseResource):
    admin_graphql_api_id: str
    callback_url: str | None
    fulfillment_orders_opt_in: bool
    handle: str
    id: int
    inventory_management: bool
    location_id: int
    name: str
    permits_sku_sharing: bool = True
    provider_id: str | None
    requires_shipping_method: bool = False
    tracking_support: bool

    class Meta:
        base_endpoint: str = '/2023-01/fulfillment_services'
        plural_name: str = 'fulfillment_services'