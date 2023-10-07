# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from headless.core import BaseCredential
from headless.types import IRequest


class RefurbishedCredential(BaseCredential):
    api_token: str

    def __init__(self, api_token: str):
        self.api_token = api_token

    async def add_to_request(self, request: IRequest[Any]) -> None:
        await super().add_to_request(request)
        request.add_header('Authorization', f'Bearer {self.api_token}')