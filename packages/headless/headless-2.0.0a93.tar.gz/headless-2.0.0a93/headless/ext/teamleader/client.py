# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import AsyncGenerator
from typing import TypeVar

from headless.core import LinearBackoff
from headless.core.httpx import Client
from headless.types import ICredential
from headless.types import IResource
from headless.types import IBackoff
from headless.types import ResourceDoesNotExist
from headless.types.iresponse import IResponse

from .createresponse import CreateResponse


M = TypeVar('M', bound=IResource)


class TeamleaderClient(Client):
    __module__: str = 'headless.ext.teamleader'
    base_url: str = "https://api.focus.teamleader.eu"
    backoff: IBackoff = LinearBackoff(5, 30)

    def __init__(self, *, credential: ICredential, **kwargs: Any):
        super().__init__(base_url=self.base_url, credential=credential, **kwargs)

    async def on_created(
        self,
        model: type[M],
        params: Any,
        response: IResponse[Any, Any]
    ) -> M:
        dto = CreateResponse.parse_obj(await response.json())
        return await self.retrieve(model, dto.data.id)

    async def retrieve(
        self,
        model: type[M],
        resource_id: int | str | None = None,
        params: dict[str, str] | None = None
    ) -> M:
        meta = model.get_meta()
        response = await self.post(
            url=model.get_retrieve_url(resource_id),
            json={'id': str(resource_id)},
            headers=meta.headers,
            params=params
        )
        if response.status_code == 404:
            raise ResourceDoesNotExist(model, response)
        response.raise_for_status()
        self.check_json(response.headers)
        data = self.process_response('retrieve', await response.json())
        return self.resource_factory(model, 'retrieve', data)
    
    async def listall(
        self,
        model: type[M],
        *args: Any,
        url: str | None = None,
        iteration: int = 0,
        params: dict[str, str] | None = None,
        allow_retry: bool = True,
    ) -> AsyncGenerator[M, None]:
        iteration += 1
        page_size: int = 100
        meta = model.get_meta()
        search: dict[str, Any] = {}
        if args:
            search = args[0]
        response = await self.request(
            method='POST',
            url=url or model.get_list_url(*args),
            json={
                **search,
                'page': {
                    'size': page_size,
                    'number': iteration
                },
                #'sort': [
                #    {
                #        'field': 'added_at',
                #        'order': 'asc'
                #    }
                #]
            },
            headers=meta.headers,
            params=params
        )
        response.raise_for_status()
        self.check_json(response.headers)
        data = self.process_response('list', await response.json())
        data = model.process_response('list', data)
        resources = [
            self.resource_factory(model, None, x)
            for x in data
        ]
        if not resources:
            return
        while resources:
            yield resources.pop(0)
        async for resource in self.listall(model, *args, iteration=iteration, params=params):
            yield resource