# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from datetime import timedelta
from datetime import timezone

import pydantic

from ..types import IObjectKey
from .bearertokencredential import BearerTokenCredential



class AccessTokenKey(IObjectKey['AccessToken']):
    __module__: str = 'headless.ext.oauth2.types'
    client_id: str
    resource: str

    def __init__(self, client_id: str, resource: str):
        self.client_id = client_id
        self.resource = resource


class AccessToken(pydantic.BaseModel):
    """Storage model for access tokens."""
    access_token: str
    client_id: str
    expires: datetime
    resource: str
    scope: set[str] = set()

    @classmethod
    def from_response(
        cls,
        client_id: str,
        resource: str,
        token: str | BearerTokenCredential,
        scope: set[str],
        ttl: int
    ):
        return cls.parse_obj({
            'access_token': str(token),
            'client_id': client_id,
            'expires': datetime.now(timezone.utc) + timedelta(seconds=ttl),
            'resource': resource,
            'scope': scope
        })

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) < self.expires
    
    def get_access_token(self) -> str:
        return self.access_token

    def get_primary_key(self) -> IObjectKey['AccessToken']:
        return AccessTokenKey(self.client_id, self.resource)
    
    def __repr__(self) -> str:
        return f"AccessToken(client_id='{self.client_id}', resource='{self.resource}')"

    def __str__(self) -> str:
        return repr(self)