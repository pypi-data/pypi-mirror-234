# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from headless.core import BaseCredential


class PlacesCredential(BaseCredential):
    __module__: str = 'headless.ext.google'
    api_key: str

    def __init__(self, api_key: str) :
        self.api_key = api_key

    async def preprocess_request(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Preprocesses the parameters used to build a request."""
        params: dict[str, str] = kwargs.setdefault('params', {})
        params['key'] = self.api_key
        return kwargs