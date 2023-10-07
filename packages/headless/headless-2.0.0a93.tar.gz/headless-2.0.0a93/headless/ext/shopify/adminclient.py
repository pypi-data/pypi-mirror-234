# Copyright (C) 2022 Cochise Ruhulessin
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

from headless.core import httpx
from headless.core import LinearBackoff
from headless.types import IBackoff
from headless.types import IResource
from .credential import ShopifyCredential


M = TypeVar('M', bound=IResource)


class AdminClient(httpx.Client):
    recover_ratelimit: bool = False
    backoff: IBackoff = LinearBackoff(5, 30)
    shopify_domain: str

    @property
    def domain(self) -> str:
        return self.shopify_domain

    def __init__(
        self,
        domain: str,
        access_token: str | None = None,
        *args: Any,
        **kwargs: Any
    ):
        self.shopify_domain = domain
        if access_token is not None:
            kwargs.setdefault('credential', ShopifyCredential(access_token))
        headers = kwargs.setdefault('headers', {})
        headers.update({
            'Accept': 'application/json'
        })
        super().__init__(
            base_url=f'https://{domain}/admin/api',
            *args,
            **kwargs
        )

    def listall(
        self,
        model: type[M],
        *args: Any,
        url: str | None = None,
        iteration: int = 0,
        params: dict[str, str] | None = None,
        allow_retry: bool = True,
    ) -> AsyncGenerator[M, None]:
        # Shopify does not accept params during pagination.
        if iteration > 0:
            params = None
        return super().listall(model, *args, url=url, iteration=iteration, params=params, allow_retry=allow_retry)