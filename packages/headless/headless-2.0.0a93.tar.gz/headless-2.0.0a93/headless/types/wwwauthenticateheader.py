# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.request
from typing import TypeVar

T = TypeVar('T')


class WWWAuthenticateHeader:
    __module__: str = 'headless.types'
    scheme: str
    params: dict[str, str]

    @classmethod
    def parse(cls: type[T], value: str) -> T:
        scheme, _, params = str.partition(value, ' ')
        if params:
            params = urllib.request.parse_keqv_list(
                urllib.request.parse_http_list(params)
            )
        return cls(scheme, params)
        
    def __init__(self, scheme: str, params: dict[str, str] | None = None):
        self.scheme = scheme
        self.params = params or {}

    def get(self, key: str) -> str | None:
        return self.params.get(key)