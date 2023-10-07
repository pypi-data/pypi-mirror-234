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
from typing import Iterable
from typing import Iterator
from typing import Mapping
from typing import TypeVar

from headless.ext.shopify.v2023_1.basemetafield import BaseMetafield

from ..adminclient import AdminClient
from .baseresource import BaseResource
from .metafield import Metafield


T = TypeVar('T')


class MetafieldSet(Mapping[str, Metafield]):
    _client: AdminClient
    _changed: set[str]
    _fields: dict[str, Metafield]
    _resource: BaseResource

    def __init__(self, client: AdminClient, resource: BaseResource,  metafields: Iterable[Metafield]):
        self._changed = set()
        self._client = client
        self._fields = {f'{x.namespace}.{x.key}': x for x in metafields}
        self._resource = resource

    def has(self, key: str) -> bool:
        return key in self._fields

    def parse(self, key: str, parser: Callable[..., T] = lambda x: x) -> T:
        return self._fields[key].parse(parser)

    async def set(self, key: str, value: Any) -> None:
        if not self.has(key):
            metafield = await self._resource.create_metafield(key, value)
        else:
            metafield = self._fields[key]
            metafield.value = value
            await metafield.persist()

    def __getitem__(self, __key: str) -> Metafield:
        return self._fields[__key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._fields)

    def __len__(self) -> int:
        return len(self._fields)