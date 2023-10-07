# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from types import NotImplementedType
from typing import TypeVar

import pydantic
from ckms.types import Malformed
from ckms.core.models import JOSEObject
from ckms.core.models import JSONWebSignature


T = TypeVar('T', bound='JSONWebToken')


class JSONWebToken(pydantic.BaseModel):
    _token: str = pydantic.PrivateAttr(None)

    @classmethod
    def parse_jwt(
        cls: type[T],
        token: str,
        accept: set[str] | NotImplementedType = NotImplemented,
        **extra: Any
    ) -> T:
        try:
            jws = JOSEObject.parse(token)
        except (Malformed, pydantic.ValidationError):
            raise ValueError('malformed JSON Web Token')
        if not isinstance(jws, JSONWebSignature):
            raise ValueError('can not interpret JOSE object')
        jwt = jws.get_claims()
        typ = jws.typ

        # TODO: This, ofcourse, is malpractice but we need it now and
        # a framework to have issuer-specific JWT rules is to be
        # implemented later.
        if jwt.iss == "https://api.login.yahoo.com":
            # Simply assume that it is a JWT since this object only parses
            # OIDC ID Tokens.
            typ = "jwt"
        if accept != NotImplemented and typ not in accept:
            raise TypeError(f'Invalid JWT type: {str(typ)[:16]}')
        self = cls.parse_obj({**jwt.dict(), **extra})
        self._token = token
        return self