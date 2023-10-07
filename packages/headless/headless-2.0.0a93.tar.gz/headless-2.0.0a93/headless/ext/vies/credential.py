# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from headless.types import BasicAuth


class VIESCredential(BasicAuth):

    def __init__(self, api_id: str, api_key: str) -> None:
        super().__init__(username=api_id, password=api_key)