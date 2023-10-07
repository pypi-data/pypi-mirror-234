# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Callable
from typing import Generic
from typing import Protocol
from typing import TypeVar

import pydantic


C = TypeVar('C')
T = TypeVar('T')


class IEncrypter(Protocol, Generic[C]):
    """Provides an interface to perform cryptographic operations with
    a set of well-defined cryptographic keys.
    """
    __module__: str = 'headless.types'

    async def decrypt(
        self,
        ct: C,
        parser: Callable[[C, bytes], T] = lambda _, pt: pt
    ) -> T:
        ...

    async def encrypt(
        self,
        pt: bytes | str | pydantic.BaseModel,
        encoding: str = 'utf-8'
    ) -> C:
        """Encrypt plain text `pt` using the default key."""
        ...