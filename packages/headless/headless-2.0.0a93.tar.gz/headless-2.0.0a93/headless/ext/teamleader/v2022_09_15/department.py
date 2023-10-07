# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from ..resource import TeamleaderResource
from .departmentemail import DepartmentEmail


class Department(TeamleaderResource):
    id: str
    name: str
    emails: list[DepartmentEmail]

    # Remainder of fields can be None

    @classmethod
    def get_retrieve_url(cls, resource_id: int | str | None) -> str:
        return f'{cls._meta.base_endpoint}.info'

    class Meta(TeamleaderResource.Meta):
        base_endpoint: str = '/departments'