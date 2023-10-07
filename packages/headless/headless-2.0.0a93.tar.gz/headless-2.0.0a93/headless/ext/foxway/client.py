# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from headless.core import httpx
from headless.core import LinearBackoff
from headless.types import IBackoff

from .credential import FoxwayCredential


class FoxwayClient(httpx.Client):
    backoff: IBackoff = LinearBackoff(5, 15)
    api_url: str = 'https://foxway.shop/api/v1'

    def __init__(
        self,
        api_key: str | None = None,
    ):
        super().__init__(
            base_url=self.api_url,
            credential=FoxwayCredential(api_key)
        )