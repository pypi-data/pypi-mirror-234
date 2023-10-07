# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

import pydantic
from canonical import ResourceName

from .iresourcemeta import IResourceMeta

T = TypeVar('T', bound='IResource')


class IResource(pydantic.BaseModel):
    __deferred__: dict[str, Any] = pydantic.PrivateAttr({})
    _meta: IResourceMeta

    @property
    def resource_name(self) -> ResourceName:
        return self.get_resource_name(self._client.domain)

    @classmethod
    def enveloped(cls, dto: dict[str, Any]) -> dict[str, Any]:
        return dto

    @classmethod
    def get_meta(cls) -> IResourceMeta:
        return cls._meta

    @classmethod
    def get_create_url(cls, *params: Any) -> str:
        return cls._meta.get_create_url()

    @classmethod
    def get_list_url(cls, *params: Any) -> str:
        return cls._meta.get_list_url()

    @classmethod
    def get_retrieve_url(
        cls: type[T],
        resource_id: int | str | None
    ) -> str:
        raise NotImplementedError
    
    @classmethod
    def process_response(cls, action: str, data: Any) -> Any:
        raise NotImplementedError

    def get_persist_url(self) -> str:
        raise NotImplementedError

    def get_resource_name(self, domain: str) -> ResourceName:
        raise NotImplementedError