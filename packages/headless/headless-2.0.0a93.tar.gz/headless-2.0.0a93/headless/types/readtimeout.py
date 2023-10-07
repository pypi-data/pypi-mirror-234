# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import logging
from typing import Any

from .iclient import IClient
from .irequest import IRequest
from .iresponse import IResponse
from .iretryable import IRetryable


class ReadTimeout(IRetryable):
    __module__: str = 'headless.types'
    client: IClient[Any, Any]
    delay: float = 1.0
    max_retries: int
    logger: logging.Logger = logging.getLogger('headless.client')
    request: IRequest[Any]

    def __init__(
        self,
        client: IClient[Any, Any],
        request: IRequest[Any],
        max_retries: int = 5
    ):
        self.client = client
        self.max_retries = max_retries
        self.request = request

    async def retry(self) -> IResponse[Any, Any]:
        """Retry the request and return the response, or re-raise the
        error if the request does not succeed within :attr:`max_attempts`.
        """
        if self.request.method not in {'HEAD', 'GET', 'OPTIONS'}:
            raise self
        for _ in range(self.max_retries):
            self.logger.warning("Caught read timeout, retrying")
            try:
                response = await self.client.send(self.request)
            except ReadTimeout:
                await asyncio.sleep(self.delay)
                continue
            break
        else:
            raise self
        return response
