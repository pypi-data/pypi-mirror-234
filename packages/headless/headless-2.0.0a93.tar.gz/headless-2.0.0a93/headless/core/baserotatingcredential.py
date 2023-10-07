# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import itertools
from typing import Any
from typing import Iterable

from headless.types import ICredential
from headless.types import IRequest
from .basecredential import BaseCredential


class BaseRotatingCredential(BaseCredential):
    __module__: str = 'headless.core'

    @property
    def next(self) -> ICredential:
        return next(self.pool)

    def __init__(self, credentials: Iterable[ICredential]):
        self.pool = itertools.cycle(credentials)

    async def add_to_request(self, request: IRequest[Any]) -> None:
        """Modify a :class:`Request` instance to include this
        credential.
        """
        await self.next.add_to_request(request)