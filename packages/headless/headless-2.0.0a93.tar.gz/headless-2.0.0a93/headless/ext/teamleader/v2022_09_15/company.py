# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import Any
from typing import Callable
from typing import TypeVar

from canonical.crm import CompanyBasicInfo

from headless.types import IClient
from ..resource import TeamleaderResource
from .companyemail import CompanyEmail
from .companyaccountmanager import CompanyAccountManager
from .companyaddress import CompanyAddress
from .companyaddessdetails import CompanyAddressDetails
from .companyphonenumber import CompanyPhonenumber
from .companycustomfield import CompanyCustomField


T = TypeVar('T', bound='Company')


class Company(TeamleaderResource):
    addresses: list[CompanyAddress] = []
    custom_fields: list[CompanyCustomField] = []
    emails: list[CompanyEmail] = []
    id: str
    name: str
    responsible_user: CompanyAccountManager | None
    tags: list[str] = []
    telephones: list[CompanyPhonenumber] = []
    vat_number: str | None = None

    @property
    def country(self) -> str:
        if not self.addresses:
            raise AttributeError("Company addresses not present.")
        if self.addresses[0].address.country is None:
            raise AttributeError("Company does not have a country specified.")
        return self.addresses[0].address.country

    @classmethod
    async def from_dto(
        cls,
        client: IClient[Any, Any],
        dto: CompanyBasicInfo,
        get_area_level_two_id: Callable[[str], str | None],
        **extra: Any
    ):
        """Create a new :class:`Company` using the :class:`canonical.CompanyBasicInfo`
        Data Transfer Object (DTO).
        """
        params: dict[str, Any] = {
            'name': dto.spec.company_name,
            'tags': list(dto.get_tags())
        }
        if dto.spec.addresses:
            addresses: list[dict[str, Any]] = []
            for address in dto.spec.addresses:
                area_level_two_id: str | None = None
                if address.spec.region:
                    area_level_two_id = get_area_level_two_id(address.spec.region)
                addresses.append({
                    'type': 'primary',
                    'address': {
                        **CompanyAddressDetails.parse_dto(address.spec)\
                            .dict(exclude={'addressee'}),
                        'area_level_two_id': area_level_two_id
                    }
                })
            params['addresses'] = addresses
        if dto.spec.phonenumbers:
            phonenumbers: list[dict[str, str]] = []
            for phonenumber in dto.spec.phonenumbers:
                phonenumbers.append({
                    'type': 'phone',
                    'number': phonenumber.value
                })
            params['telephones'] = phonenumbers

        if dto.has_annotation('account-manager', namespace='teamleader.eu'):
            params['responsible_user_id'] = dto.get_annotation(
                name='account-manager',
                namespace='teamleader.eu'
            )

        if dto.spec.website:
            params['website'] = dto.spec.website

        params.update(extra)
        return await client.create(cls, params)

    @classmethod
    def get_create_url(cls, *params: Any) -> str:
        return f'{cls._meta.base_endpoint}.add'

    @classmethod
    def get_retrieve_url(cls: type[T], resource_id: int | str | None) -> str:
        return f'{cls._meta.base_endpoint}.info'

    def get_field(self, field_id: str) -> Any:
        for field in self.custom_fields:
            if field.definition.id != field_id:
                continue
            value = field.value
            break
        else:
            raise AttributeError(f"No such field: {field_id}")
        return value

    def has_field(self, field_id: str) -> bool:
        return any([x.definition.id == field_id for x in self.custom_fields])

    def is_tagged(self, name: str) -> bool:
        """Return a boolean indicating if the company has the given tag."""
        return name in self.tags

    async def refresh(self) -> None:
        obj = await self._client.retrieve(type(self), self.id)
        for field in obj.__fields__.values():
            setattr(self, field.name, getattr(obj, field.name))

    async def set_fields(self, data: dict[str, Any]):
        """Set the given fields to the given values."""
        # TODO: The list endpoint does not return all objects.
        obj = await self._client.retrieve(type(self), self.id)
        provided: set[str] = {x for x in data.keys()}
        self.custom_fields = obj.custom_fields
        fields = [
            {'id': field.definition.id, 'value': field.value}
            for field in self.custom_fields
            if field.definition.id not in provided
        ]
        for field_id, value in data.items():
            if isinstance(value, (datetime.datetime, datetime.date)):
                value = value.isoformat()
            fields.append({'id': field_id, 'value': value})
        await self._client.persist(type(self), self, data={
            'id': self.id,
            'custom_fields': fields
        })

    class Meta(TeamleaderResource.Meta): # type: ignore
        base_endpoint: str = '/companies'

    def __hash__(self) -> int: # type: ignore
        return hash(self.id)