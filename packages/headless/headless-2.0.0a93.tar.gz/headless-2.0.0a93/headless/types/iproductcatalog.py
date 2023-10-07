# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Any
from typing import Generic
from typing import Iterator
from typing import TypeVar

from .iclient import IClient


T = TypeVar('T')


class IProductCatalog(Generic[T]):
    __module__: str = 'headless.types'
    client: IClient[Any, Any]
    logger: logging.Logger = logging.getLogger('headless')
    model: type[T]

    async def retrieve(self) -> None: ...
    def get_by_sku(self, sku: str) -> T | None: ...
    def get_by_product_id(self, product_id: int | str) -> T | None: ...
    def __iter__(self) -> Iterator[T]: ...