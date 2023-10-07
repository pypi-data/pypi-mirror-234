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

from headless.core import Resource
from headless.types import IClient
from headless.types import IResponse


T = TypeVar('T', bound='ShopifyResource')


class ShopifyResource(Resource):
    __abstract__: bool = True

    @staticmethod
    def camel_to_snake(name):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @classmethod
    def get_list_url(cls, *params: Any) -> str:
        url = super().get_list_url(*params) + '.json'
        if params:
            url = url.format(*params)
        return url

    @classmethod
    def get_next_url(
        cls,
        response: IResponse[Any, Any],
        n: int
    ) -> str | None:
        if not response.headers.get('link'):
            return
        value = response.headers.get('link')
        for link in str.split(value, ','):
            link = str.strip(link)
            m = re.match('<(?P<url>[^>]+)>; rel="(?P<rel>next|previous)"', link)
            if not m:
                continue
            params = m.groupdict()
            if not params.get('rel') == 'next':
                continue
            url = params['url']
            break
        else:
            url = None
        return url
    
    @classmethod
    def get_retrieve_url(cls: type[T], resource_id: int | str | None) -> str:
        return f'{cls._meta.base_endpoint}/{resource_id}.json'

    @classmethod
    def parse_resource(cls: type[T], obj: Any) -> T:
        meta = cls.get_meta()
        return super().parse_resource(obj[str.lower(meta.name)])

    @classmethod
    def process_response(
        cls,
        action: str,
        data: dict[str, Any]
    ) -> dict[str, Any]:
        if action in {'list'}:
            k = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls._meta.pluralname)
        elif action in {'retrieve'}:
            k = cls._meta.name
        elif action is None:
            return data
        else:
            raise NotImplementedError
        return data[str.lower(k)]

    @classmethod
    async def create(
        cls: type[T],
        client: IClient[Any, Any],
        params: Any
    ) -> T:
        meta = cls.get_meta()
        envelope_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls._meta.name)
        return await super().create(client, {str.lower(envelope_name): params})

    @classmethod
    def get_metafields_url(cls, resource_id: int) -> str:
        raise NotImplementedError