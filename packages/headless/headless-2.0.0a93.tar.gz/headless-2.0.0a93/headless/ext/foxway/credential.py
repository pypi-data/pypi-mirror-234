# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from typing import Any

from headless.core import BaseCredential
from headless.types import IRequest


class FoxwayCredential(BaseCredential):
    __module__: str = 'headless.ext.foxway'
    api_key: str

    def __init__(self, api_key: str | None = None):
        api_key = api_key or os.getenv('FOXWAY_API_KEY')
        if api_key is None:
            raise ValueError("Unable to discover Foxway API credentials.")
        self.api_key = api_key

    async def add_to_request(self, request: IRequest[Any]) -> None:
        await super().add_to_request(request)
        request.add_header('X-ApiKey', self.api_key)