# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .baseclient import BaseClient


class TestClient(BaseClient):
    __module__: str = 'headless.ext.refurbed'

    def get_base_url(self, base_url: str) -> str:
        return "https://grpc-refurbplatform.qa.refurbed.io"