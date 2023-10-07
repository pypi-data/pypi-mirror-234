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

import pydantic

from ..resource import ShopifyResource


class Webhook(ShopifyResource):
    address: str
    fields: list[str] = []
    format: str = 'json'
    metafield_namespaces: list[str] = []
    private_metafield_namespaces: list[str] = []
    topic: str

    # Readonly
    api_version: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: int

    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        values.update({
            'fields': values.get('fields') or [],
            'metafield_namespaces': values.get('metafield_namespaces') or [],
            'private_metafield_namespaces': (
                values.get('private_metafield_namespaces') or []
            )
        })
        return values

    def get_persist_url(self) -> str:
        return self.get_retrieve_url(self.id)

    class Meta:
        base_endpoint: str = '/2023-01/webhooks'