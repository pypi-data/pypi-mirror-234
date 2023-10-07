# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar


T = TypeVar('T', bound='ResourceExceptionType')


class ResourceExceptionType(type):
    __module__: str = 'headless.types'

    def __new__(
        cls: type[T],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **params: dict[str, Any]
    ) -> T:
        return super().__new__(cls, name, bases, namespace, **params) # type: ignore