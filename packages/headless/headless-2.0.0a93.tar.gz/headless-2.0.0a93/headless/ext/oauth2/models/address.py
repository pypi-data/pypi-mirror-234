# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic
from canonical import ISO3166Alpha2


class Address(pydantic.BaseModel):
    formatted: str | None = pydantic.Field(
        default=None,
        title="Formatted",
        description=(
            "Full mailing address, formatted for display or use on a "
            "mailing label. This field MAY contain multiple lines, "
            "separated by newlines. Newlines can be represented either "
            "as a carriage return/line feed pair (`\\r\\n`) or as a "
            "single line feed character (`\\n`)."
        )
    )

    street_address: str | None = pydantic.Field(
        default=None,
        title="Street address",
        description=(
            "Full street address component, which MAY include house number, "
            "street name, Post Office Box, and multi-line extended street "
            "address information. This field MAY contain multiple lines, "
            "separated by newlines. Newlines can be represented either as "
            "a carriage return/line feed pair (`\\r\\n`) or as a single "
            "line feed character (`\\n`)."
        )
    )

    locality: str | None = pydantic.Field(
        default=None,
        title="Locality",
        description="City or locality component."
    )

    region: str | None = pydantic.Field(
        default=None,
        title="Region",
        description="State, province, prefecture, or region component."
    )

    postal_code: str | None = pydantic.Field(
        default=None,
        title="Postal code",
        description="Zip code or postal code component."
    )

    country: ISO3166Alpha2 | str | None = pydantic.Field(
        default=None,
        title="Country",
        description="Country name component."
    )

    # The following members are non-standard attributes supported
    # by this module.
    longitude: float | None = pydantic.Field(
        default=None,
        title="Longitude",
        description="Longitude of the address, in degrees (WGS84)"
    )

    latitude: float | None = pydantic.Field(
        default=None,
        title="Latitude",
        description="Latitude of the address, in degrees (WGS84)"
    )

    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        if values.get('longitude') is not None and values.get('latitude') is None:
            raise ValueError("latitude is a required claim if longitude is provided.")
        if values.get('latitude') is not None and values.get('longitude') is None:
            raise ValueError("longitude is a required claim if latitude is provided.")
        return values