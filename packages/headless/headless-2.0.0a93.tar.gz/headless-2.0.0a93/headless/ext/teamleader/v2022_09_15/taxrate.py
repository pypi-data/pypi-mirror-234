# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from ..resource import TeamleaderResource

from .resourcereference import ResourceReference


class Taxrate(TeamleaderResource):
    id: str
    description: str
    rate: float
    department: ResourceReference

    @classmethod
    def get_retrieve_url(cls, resource_id: int | str | None) -> str:
        return f'{cls._meta.base_endpoint}.info'

    class Meta(TeamleaderResource.Meta):
        base_endpoint: str = '/taxRates'