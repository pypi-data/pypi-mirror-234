# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from headless.core.httpx import Client


class WooCommerceClient(Client):
    __module__: str = 'headless.ext.woocommerce'

    def get_base_url(self, base_url: str) -> str:
        return f'{base_url}/wp-json/wc/v3'