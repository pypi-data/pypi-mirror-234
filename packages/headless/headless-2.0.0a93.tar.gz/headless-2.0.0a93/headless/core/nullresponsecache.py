# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import json
import pathlib
from typing import Any

from headless.types import IResponseCache


class NullResponseCache(IResponseCache):
    __module__: str = 'headless.core'

    async def get(self, key: str) -> Any:
        return None

    async def set(self, key: str, value: Any) -> None:
        pass