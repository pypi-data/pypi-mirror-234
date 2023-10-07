# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic
from canonical import GenericDeliveryPointSpecification
from canonical import ISO3166Alpha2
from canonical import Phonenumber

from .addresscomponent import AddressComponent
from .geometry import Geometry
from .placeditorialsummary import PlaceEditorialSummary
from .placeopeninghours import PlaceOpeningHours
from .placephoto import PlacePhoto
from .pluscode import PlusCode


class Place(pydantic.BaseModel):
    address_components: list[AddressComponent] = []
    adr_address: str | None = None
    business_status: str | None = None
    curbside_pickup: bool = False
    current_opening_hours: PlaceOpeningHours | None = None
    delivery: bool = False
    dine_in: bool = False
    editorial_summary: PlaceEditorialSummary | None = None
    formatted_address: str | None = None
    formatted_phone_number: str | None = None
    geometry: Geometry | None = None
    icon: str | None = None
    icon_background_color: str | None = None
    icon_mask_base_uri: str | None = None
    international_phone_number: Phonenumber | None = None
    name: str
    opening_hours: PlaceOpeningHours | None = None
    place_id: str
    photos: list[PlacePhoto] = []
    plus_code: PlusCode | None = None
    price_level: int | None = None
    rating: int | None = None
    reservable: bool = False
    # reviews
    secondary_opening_hours: list[PlaceOpeningHours] | None = None
    serves_beer: bool = False
    serves_breakfast: bool = False
    serves_brunch: bool = False
    serves_dinner: bool = False
    serves_lunch: bool = False
    serves_vegetarian_food: bool = False
    serves_wine: bool = False
    takeout: bool = False
    types: list[str] = []
    url: str | None = None
    user_ratings_total: int | None = None
    utc_offset: int | None = None
    vicinity: str | None = None
    website: str | None = None
    wheelchair_accessible_entrance: bool = False

    @property
    def country(self) -> ISO3166Alpha2 | None:
        for component in self.address_components:
            if 'country' not in component.types:
                continue
            country = ISO3166Alpha2(component.short_name)
            break
        else:
            country = None
        return country

    def get_address_component(
        self,
        kind: str,
        alternatives: dict[str, str] | None = None
    ) -> str:
        alternatives = alternatives or {}
        value = None
        for component in self.address_components:
            if not component.has_type({kind}):
                continue
            value = component.long_name
            break
        else:
            raise LookupError
        return alternatives.get(str.lower(value)) or value

    def get_canonical_address(self) -> GenericDeliveryPointSpecification | None:
        """Convert the :attr:`address_components` of the :class:`Place` to a
        canonical format.
        """
        # If the country is not known at all, then we have no way to construct
        # a valid address.
        country = self.country
        if country is None:
            return None

        #: See https://developers.google.com/maps/documentation/geocoding/requests-geocoding#Types
        spec = GenericDeliveryPointSpecification.parse_obj({
            'address1': '',
            'postal_code': '',
            'city': '',
            'country': self.country
        })
        street_address: list[AddressComponent] = []
        for component in self.address_components:
            # route and street_number need to be merged.
            if component.has_type({'route', 'street_number', 'premise', 'subpremise', 'floor'}):
                street_address.append(component)
                continue
            component.add_to_delivery_point(country, spec)

        if street_address and len(street_address) >= 2:
            street_address = list(sorted(street_address, key=lambda x: x.sorting_key()))
            route = street_address.pop(0)
            spec.address1 = route.short_name or route.long_name
            for component in street_address:
                spec.address1 = component.append_to_line(country, spec.address1)
        return spec