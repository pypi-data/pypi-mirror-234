# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime

from .baseresource import BaseResource


class Location(BaseResource):
    active: bool
    address1: str | None = None
    address2: str | None = None
    city: str | None = None
    country: str | None = None
    country_code: str | None = None
    created_at: datetime
    id: int
    legacy: bool = False
    name: str
    phone: str | None = None
    province: str | None = None

    class Meta:
        base_endpoint: str = '/2023-01/locations'