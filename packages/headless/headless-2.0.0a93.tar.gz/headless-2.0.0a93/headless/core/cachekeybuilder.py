# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import copy
import functools
import hashlib
import struct
from typing import cast
from typing import Any


class CacheKeyBuilder:
    __module__: str = 'headless.core'

    def build(self, *args: Any, **kwargs: Any) -> str:
        h = hashlib.sha3_256()
        for a in args:
            h.update(self.to_bytes(copy.deepcopy(a)))
        for k in sorted(kwargs.keys()):
            h.update(self.to_bytes(k))
            h.update(self.to_bytes(copy.deepcopy(kwargs[k])))
        return h.hexdigest()

    @functools.singledispatchmethod
    def to_bytes(self, obj: Any) -> bytes:
        raise TypeError(type(obj).__name__)

    @to_bytes.register
    def bytes_from_dict(self, value: dict) -> bytes: # type: ignore
        h = hashlib.sha3_256()
        for k in sorted(cast(dict[Any, Any], value.keys())):
            h.update(self.to_bytes(k))
            h.update(self.to_bytes(value[k]))
        return h.digest()

    @to_bytes.register
    def bytes_from_float(self, value: float) -> bytes:
        return struct.pack('d', value)

    @to_bytes.register
    def bytes_from_string(self, value: str) -> bytes:
        return str.encode(value)