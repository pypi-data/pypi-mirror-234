# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from canonical import GenericDeliveryPointSpecification
from canonical import GenericPostalAddress


class CompanyAddressDetails(pydantic.BaseModel):
    addressee: str | None = None
    city: str | None = None
    country: str | None = None
    line_1: str | None = None
    postal_code: str | None = None

    @classmethod
    def parse_dto(
        cls,
        dto: GenericPostalAddress | GenericDeliveryPointSpecification
    ):
        params: dict[str, str] = {
            **dto.dict(include={'city', 'country', 'postal_code'}),
            'line_1': dto.address1
        }
        if isinstance(dto, GenericPostalAddress) and dto.contact_name:
            params['addressee'] = dto.contact_name
        return cls.parse_obj(params)