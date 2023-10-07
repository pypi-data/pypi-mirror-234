# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from .placeopeninghoursperiod import PlaceOpeningHoursPeriod
from .placespecialday import PlaceSpecialDay


class PlaceOpeningHours(pydantic.BaseModel):
    open_now: bool = False
    periods: list[PlaceOpeningHoursPeriod] = []
    special_days: list[PlaceSpecialDay] = []
    type: str | None = None
    weekday_text: list[str] = []