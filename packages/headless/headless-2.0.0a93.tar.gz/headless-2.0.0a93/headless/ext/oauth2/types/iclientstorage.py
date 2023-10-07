# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Protocol
from typing import TypeAlias
from typing import TypeVar

from .iobjectkey import IObjectKey


ClientObject = TypeVar('ClientObject')


class IClientStorage(Protocol):
    __module__: str = 'headless.ext.oauth2.types'
    ObjectType: TypeAlias = ClientObject

    async def get(self, key: IObjectKey[ClientObject]) -> ClientObject | None: ...