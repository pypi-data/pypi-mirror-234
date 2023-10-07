# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import AsyncIterator

from headless.core.httpx import Client
from headless.core import LinearBackoff
from headless.types import IBackoff
from .models import Place
from .models import PlacesDetailsResponse
from .models import PlacesNearbySearchResponse
from .placescredential import PlacesCredential


class PlacesClient(Client):
    __module__: str = 'headless.ext.google'
    backoff: IBackoff = LinearBackoff(5, 30)

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = 'https://maps.googleapis.com/',
        **kwargs: Any
    ):
        credential = PlacesCredential(api_key)
        super().__init__(base_url=base_url, credential=credential, **kwargs)

    async def nearby(
        self,
        latitude: str,
        longitude: str,
        keyword: str | None = None,
        kind: str | None = None,
        radius: int = 500,
        pagetoken: str | None = None
    ) -> AsyncIterator[Place]:
        """Performce a nearby search for the given keyword."""
        url = '/maps/api/place/nearbysearch/json'
        params: dict[str, str | None] = {
            'location': f'{latitude},{longitude}',
            'radius': str(radius),
            'keyword': keyword,
            'pagetoken': pagetoken,
            'type': kind
        }
        params = {k: v for k, v in params.items() if v is not None}
        key, cached = await self.from_cache('GET', url, params)
        assert key is not None
        if cached is not None:
            dto = PlacesNearbySearchResponse.parse_raw(cached)
            for obj in dto.results:
                yield obj
        else:
            response = await self.get(url=url, params=params)
            dto = PlacesNearbySearchResponse.parse_obj(await response.json())
            await self.to_cache(key, dto.json())
            for obj in dto.results:
                yield obj
            if dto.next_page_token:
                async for obj in self.nearby(latitude, longitude, pagetoken=dto.next_page_token):
                    yield obj
    
    async def detail(
        self,
        place_id: str,
        fields: set[str] | None = None,
        place: Place | None = None,
        phonenumber: bool = False,
        opening_hours: bool = False,
        current_opening_hours: bool = False,
        secondary_opening_hours: bool = False,
        website: bool = False
    ) -> Place | None:
        """Lookup a :class:`~headless.ext.google.models.Place` instance
        by its identifier.

        Base cost is USD 0.017. Contact fields are billed by Google for
        an amount of USD 0.003 *per field*.

        Args:
            phonenumber (bool): retrieve the internationally formatted
                phonenumber of the place.
            current_opening_hours (bool): retrieve the hours of operation
                for the coming seven days.
            opening_hours (bool): retrieve the regular hours of operation.
            secondary_opening_hours (bool): retrieve the hours of operation
                for the coming seven days, including hours during which
                exceptions apply (such as drive-through only).
            website (bool): retrieve the website.
        """
        # See https://developers.google.com/maps/documentation/places/web-service/usage-and-billing/#contact-data
        default_fields: set[str] = {
            # Basic fields only by default.
            # See https://developers.google.com/maps/documentation/places/web-service/details#fields
            'address_components',
            'adr_address',
            'business_status',
            'formatted_address',
            'geometry',
            'icon',
            'icon_mask_base_uri',
            'icon_background_color',
            'name',
            'photo',
            'place_id',
            'plus_code',
            'type',
            'url',
            'utc_offset',
            'vicinity',
            'wheelchair_accessible_entrance'
        }
        fields = set(fields or default_fields)
        if phonenumber:
            fields.add('international_phone_number')
        if current_opening_hours:
            fields.add('current_opening_hours')
        if opening_hours:
            fields.add('opening_hours')
        if secondary_opening_hours:
            fields.add('secondary_opening_hours')
        if website:
            fields.add('website')
        params: dict[str, str] = {'place_id': place_id, 'fields': str.join(',', sorted(fields))}
        url: str = '/maps/api/place/details/json'

        key, cached = await self.from_cache('GET', url, params)
        if cached is not None:
            dto = PlacesDetailsResponse.parse_raw(cached)
            return dto.result
        else:
            response = await self.get(url=url, params=params)
            dto = PlacesDetailsResponse.parse_obj(await response.json())
            if dto.result is None and dto.status != "NOT_FOUND":
                raise NotImplementedError(dto.status)
            await self.to_cache(key, dto.json())
            if dto.result is None:
                return None
            return Place.parse_obj({
                'place_id': place_id,
                **(place.dict(exclude_none=True) if place else {}),
                **(dto.result.dict(exclude_none=True) if dto.result else {}),
            })