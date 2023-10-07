# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .baseresource import BaseResource
from .basemetafield import BaseMetafield


class Metafield(BaseResource, BaseMetafield):

    def get_persist_url(self) -> str:
        return self.get_retrieve_url(self.id)

    class Meta:
        base_endpoint: str = '/2023-01/metafields'