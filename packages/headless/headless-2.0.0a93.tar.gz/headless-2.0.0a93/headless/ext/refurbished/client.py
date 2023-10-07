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

from headless.core import httpx
from headless.core import LinearBackoff
from headless.types import IBackoff
from headless.types import IResponse
from headless.types import IResource
from .credential import RefurbishedCredential


M = TypeVar('M', bound=IResource)


class RefurbishedClient(httpx.Client):
    backoff: IBackoff = LinearBackoff(5, 15)

    def __init__(
        self,
        api_token: str,
        api_url: str = "https://connect.refurbished.nl/api"
    ):
        super().__init__(
            base_url=api_url,
            credential=RefurbishedCredential(api_token)
        )


    async def on_created(
        self,
        model: type[M],
        params: Any,
        response: IResponse[Any, Any]
    ) -> M:
        data = await response.json()
        if data.get('errors'):
            raise Exception(f"Operation failed: {data['errors']}")
        raise NotImplementedError