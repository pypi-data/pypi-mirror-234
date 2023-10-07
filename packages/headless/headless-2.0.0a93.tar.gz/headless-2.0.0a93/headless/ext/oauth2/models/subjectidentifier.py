# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import base64
import hashlib

import pydantic


class SubjectIdentifier(pydantic.BaseModel):
    __module__: str = 'headless.ext.oauth2'
    iss: str
    sub: str

    @property
    def sha256(self) -> str:
        h = hashlib.sha3_256()
        h.update(str.encode(type(self).__name__))
        h.update(str.encode(self.iss))
        h.update(str.encode(self.sub))
        return bytes.decode(base64.urlsafe_b64encode(h.digest()))