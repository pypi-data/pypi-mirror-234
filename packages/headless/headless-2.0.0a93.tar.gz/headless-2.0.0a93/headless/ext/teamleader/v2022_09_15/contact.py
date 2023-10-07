# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

from ..resource import TeamleaderResource
from .contactcustomfield import ContactCustomField
from .contactemail import ContactEmail

T = TypeVar('T', bound='Contact')


class Contact(TeamleaderResource):
    custom_fields: list[ContactCustomField] = []
    first_name: str | None = None
    emails: list[ContactEmail] = []
    id: str
    last_name: str
    status: str
    tags: list[str] = []

    @classmethod
    def get_create_url(cls, *params: Any) -> str:
        return f'{cls._meta.base_endpoint}.add'

    @classmethod
    def get_link_url(cls) -> str:
        return f'{cls._meta.base_endpoint}.linkToCompany'

    def get_field(self, field_id: str) -> Any:
        for field in self.custom_fields:
            if field.definition.id != field_id:
                continue
            value = field.value
            break
        else:
            raise AttributeError(f"No such field: {field_id}")
        return value

    async def link_company(self, company_id: str, decision_maker: bool = False):
        response = await self._client.post(
            url=self.get_link_url(),
            json={
                'id': self.id,
                'company_id': company_id,
                'decision_maker': decision_maker
            }
        )
        response.raise_for_status()


    class Meta(TeamleaderResource.Meta): # type: ignore
        base_endpoint: str = '/contacts'