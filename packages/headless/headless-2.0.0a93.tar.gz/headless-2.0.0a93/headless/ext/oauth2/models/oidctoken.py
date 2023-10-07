# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from canonical import EmailAddress

from .claimset import ClaimSet
from .subjectidentifier import SubjectIdentifier


class OIDCToken(ClaimSet):
    iss: str
    sub: str
    exp: int
    aud: str | list[str]
    iat: int
    auth_time: int | None = None
    nonce: str | None = None
    acr: str = "0"
    amr: list[str] = []
    azp: str | None = None
    at_hash: str | None = None
    c_hash: str | None = None

    # TODO: These are WebIAM claims
    icg: bool | None = None
    uai: str | None = None

    @property
    def principals(self) -> list[EmailAddress | SubjectIdentifier]:
        values = [
            self.email,
            SubjectIdentifier(iss=self.iss, sub=self.sub) if self.sub else None
        ]
        return [x for x in values if x is not None]

    @property
    def subject(self) -> SubjectIdentifier:
        return SubjectIdentifier(iss=self.iss, sub=self.sub)

    def claims(self) -> ClaimSet:
        return ClaimSet.parse_obj(self)