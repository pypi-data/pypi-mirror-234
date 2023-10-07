# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from collections import defaultdict

import pydantic
from canonical import GenericDeliveryPointSpecification
from canonical import ISO3166Alpha2


WEIGHTS: defaultdict[str, int] = defaultdict(lambda: 0, {
    'route'         : -2,
    'street_number' : -1,
    'premise'       : 0,
    'subpremise'    : 1,
    'floor'         : 2
})


#: List which administrative division level is used as the
#: region in an address specification. None means that the
#: country does not use regions in its addressing.
REGION_LEVELS: defaultdict[str, str | None] = defaultdict(
    lambda: 'administrative_area_level_1',
    {
        'BE': 'administrative_area_level_2',
        'FR': 'administrative_area_level_2',
        'ES': 'administrative_area_level_2',
        'GB': 'administrative_area_level_3',
        'NL': 'administrative_area_level_1',
        'IT': 'administrative_area_level_2'
    }
)


IGNORED: defaultdict[str, set[str]] = defaultdict(
    lambda: {'political'},
    {
        'DE': {'administrative_area_level_3'},
        'NL': {'administrative_area_level_3'},
        'IT': {'administrative_area_level_3'}
    }
)


COUNTRY_ATTRIBUTES: defaultdict[str, dict[str, str]] = defaultdict(
    dict,
    {
        'IE': {
            'postal_town': 'city',
            'subpremise': 'address2',
        },
        'GB': {
            'postal_town': 'city',
            'route': 'address1',
        }
    }
)


class AddressComponent(pydantic.BaseModel):
    long_name: str
    short_name: str
    types: list[str]

    def add_to_delivery_point(self, country: str, spec: GenericDeliveryPointSpecification) -> None:
        """Add the :class:`AddressComponent` to a delivery point specificaion
        representing by a :class:`canonical.GenericDeliveryPointSpecification`
        object.
        """
        # https://developers.google.com/maps/documentation/geocoding/requests-geocoding#Types
        region_administrative_area = REGION_LEVELS[country]
        for kind in self.types:
            if kind in IGNORED[country]:
                continue
            attname = COUNTRY_ATTRIBUTES[country].get(kind)
            if attname is not None:
                setattr(spec, attname, self.long_name)
                continue

            match kind:
                case "administrative_area_level_1":
                    # indicates a first-order civil entity below the country level. Within
                    # the United States, these administrative levels are states. Not all
                    # nations exhibit these administrative levels. In most cases,
                    # administrative_area_level_1 short names will closely match ISO 3166-2
                    # subdivisions and other widely circulated lists; however this is
                    # not guaranteed
                    if region_administrative_area == "administrative_area_level_1":
                        spec.region = self.long_name
                case "administrative_area_level_2":
                    # indicates a second-order civil entity below the country level.
                    # Within the United States, these administrative levels are
                    # counties. Not all nations exhibit these administrative levels.
                    if region_administrative_area == "administrative_area_level_2":
                        spec.region = self.long_name
                    continue
                case "establishment":
                    continue
                case "street_address":
                    # indicates a precise street address.
                    spec.address1 = self.short_name
                case "postal_code_prefix":
                    if country != 'PT':
                        raise NotImplementedError(self)
                    spec.postal_code = self.long_name
                case "postal_code":
                    # indicates a postal code as used to address postal mail
                    # within the country.
                    spec.postal_code = self.long_name
                case "country":
                    # indicates the national political entity, and is typically
                    # the highest order type returned by the Geocoder.
                    spec.country = ISO3166Alpha2(self.short_name)
                case "locality":
                    # indicates an incorporated city or town political entity.
                    spec.city = self.long_name
                case "neighborhood":
                    continue
                case "sublocality":
                    continue
                case "sublocality_level_1":
                    continue
                case "point_of_interest":
                    continue
                case "political":
                    continue
                case "premise":
                    continue
                case _:
                    if country == "NL" and kind in {"sublocality_level_1", "sublocality"}:
                        continue
                    raise NotImplementedError(country, kind, self)

    def append_to_line(self, country: str, line: str) -> str:
        """Appends the component to an address line."""
        if self.has_type({'floor', 'subpremise'}) and country == 'ES':
            line = f'{line}, {self.long_name}'
        elif self.has_type({'premise'}) and country == 'ES':
            line = f'{line}, {self.long_name}'
        elif self.has_type({'floor', 'subpremise'}) and country == 'PT':
            line = f'{line} {self.long_name}'
        elif self.has_type({'street_number'}):
            line = f'{line} {self.long_name}'
        elif self.has_type({'premise', 'subpremise'}) and country in {'DE', 'FR', 'IE', 'IT', 'GB'}:
            line = f'{line} {self.long_name}'
        elif self.has_type({'premise', 'subpremise'}) and country == 'NL':
            pass
        elif self.has_type({'subpremise'}) and country in {'BE', 'IE'}:
            pass
        elif self.has_type({'subpremise'}) and country == 'DE':
            pass
        elif self.has_type({'route'}) and country == 'GB':
            line = f'{line}/{self.long_name}'
        else:
            raise NotImplementedError(country, self)
        return line

    def has_type(self, types: set[str]) -> bool:
        return bool(set(self.types) & types)
    
    def sorting_key(self) -> int:
        d = 0
        for kind in self.types:
            k = WEIGHTS[kind]
            if not k:
                continue
            # implies ascending sort
            if k < d:
                d = k
        return d
