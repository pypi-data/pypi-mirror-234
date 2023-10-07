# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
import urllib.parse
from typing import Any

import inflect

from headless.types import IResourceMeta


engine: inflect.engine = inflect.engine()


class ResourceMeta(IResourceMeta):
    __module__: str = 'headless.core'
    base_endpoint: str
    content_type: str
    headers: dict[str, str]
    meta: Any
    name: str
    persist_method: str
    pluralname: str

    @staticmethod
    def camel_to_snake(name: str):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @classmethod
    def frominnermeta(cls, name: str, meta: type) -> 'ResourceMeta':
        name = getattr(meta, 'name', name)
        if not isinstance(name, str):
            raise TypeError(f'{meta.__name__}.name must be a string.')
        params: dict[str, Any] = {}
        params['base_endpoint'] = base_endpoint = getattr(meta, 'base_endpoint', None)
        params.update({
            'content_type': getattr(meta, 'content_type', 'application/json'),
            'headers': getattr(meta, 'headers', {}),
            'name': getattr(meta, 'name', cls.camel_to_snake(name)),
            'pluralname': getattr(meta, 'pluralname', engine.plural_noun(name)),
            'persist_method': getattr(meta, 'persist_method', 'PUT'),
            'meta': meta
        })
        if base_endpoint is None:
            raise TypeError(f'{meta.__name__}.base_endpoint is not defined.')
        if not str.startswith(base_endpoint, '/'):
            raise ValueError(f'{meta.__name__}.base_endpoint must start with a slash')
        if str.endswith(base_endpoint, '/'):
            raise ValueError(f'{meta.__name__}.base_endpoint must not end with a slash')
        return cls(**params)

    def __init__(
        self,
        meta: Any,
        name: str,
        content_type: str,
        persist_method: str,
        pluralname: str,
        base_endpoint: str,
        headers: dict[str, str]
    ):
        self.base_endpoint = base_endpoint
        self.content_type = content_type
        self.headers = headers
        self.meta = meta
        self.name = name
        self.persist_method = persist_method
        self.pluralname = pluralname

    def clone(self, name: str):
        return self.frominnermeta(name, self.meta)

    def get_create_url(self, **params: Any) -> str:
        return self.base_endpoint

    def get_delete_url(self, resource_id: int | str | None) -> str:
        """Return the URL to delete a single instance of the resource.
        The default implementation returns :meth:`get_retrieve_url()`.
        """
        return self.get_retrieve_url(resource_id=resource_id)

    def get_retrieve_url(self, resource_id: int | str | None) -> str:
        """Return the URL to retrieve a single instance of the
        resource. This is a relative URL to the API base endpoint
        that is configured with a client instance.
        """
        if resource_id is None:
            raise TypeError("The `resource_id` parameter can not be None.")
        return f'{self.base_endpoint}/{resource_id}'

    def get_list_url(self, **params: Any) -> str:
        """Return the URL to retrieve a list of instances of the
        resource. This is a relative URL to the API base endpoint
        that is configured with a client instance.
        """
        qs = None
        if params:
            qs = f'?{urllib.parse.urlencode(params)}'
        return f'{self.base_endpoint}{qs or ""}'