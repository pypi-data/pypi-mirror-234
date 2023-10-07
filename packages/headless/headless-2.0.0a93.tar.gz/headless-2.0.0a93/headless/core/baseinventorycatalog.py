# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import AsyncIterator
from typing import Generic
from typing import TypeVar

from headless.types import IClient
from headless.types import IResource


T = TypeVar('T', bound=IResource)


class BaseInventoryCatalog(Generic[T]):
    __module__: str = 'headless.core'
    client: IClient[Any, Any]
    model: type[T]

    @classmethod
    async def load(cls, client: IClient[Any, Any]):
        catalog = cls()
        catalog.client = client
        async for resource in cls.listall(client):
            catalog.add(resource)
        return catalog

    @classmethod
    def listall(cls, client: IClient[Any, Any]) -> AsyncIterator[T]:
        return client.listall(cls.model)

    def add(self, obj: T) -> None:
        raise NotImplementedError