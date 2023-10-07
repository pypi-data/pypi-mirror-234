# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.parse
from typing import Any
from typing import TypeVar

from headless.core import Resource
from headless.types import IResponse


T = TypeVar('T', bound='WooCommerceResource')


class WooCommerceResource(Resource):
    __abstract__: bool = True

    @classmethod
    def get_next_url(
        cls,
        response: IResponse[Any, Any],
        n: int
    ) -> str | None:
        """Return the next URL when paginating, or ``None`` if there is
        no next URL.
        """
        return response.links.get('next')