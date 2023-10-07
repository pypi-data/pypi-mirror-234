# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Protocol
from typing import TypeVar

from .iobjectkey import IObjectKey


T = TypeVar('T')


class IPersistedAccessToken(Protocol):
    def get_primary_key(self: T) -> IObjectKey[T]: ...
    def is_expired(self) -> bool: ...