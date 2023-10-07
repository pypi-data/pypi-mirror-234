# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
from typing import Any
from typing import TypeVar

from ..resource import ShopifyResource


T = TypeVar('T', bound='ShopifyResource')


class BaseResource(ShopifyResource):
    __abstract__: bool = True
    id: int

    @classmethod
    def enveloped(cls, dto: dict[str, Any]) -> dict[str, Any]:
        return {cls.camel_to_snake(cls.__name__): dto}

    @classmethod
    def get_create_url(cls, *params: Any) -> str:
        return f'{super().get_create_url(*params)}.json'

    def get_persist_url(self) -> str:
        return f'{self._meta.base_endpoint}/{self.id}.json'

    @classmethod
    def parse_resource(cls: type[T], obj: Any) -> T:
        return cls.parse_obj(obj[cls.camel_to_snake(cls.__name__)])