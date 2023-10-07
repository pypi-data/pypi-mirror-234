# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import json
from datetime import datetime
from typing import Callable
from typing import TypeVar

import pydantic


T = TypeVar('T')


class BaseMetafield(pydantic.BaseModel):
    created_at: datetime
    description: str | None = None
    id: int
    key: str
    namespace: str
    owner_id: int
    owner_resource: str
    updated_at: datetime
    value: str
    type: str

    def parse(self, parser: Callable[..., T] = lambda x: x ) -> T:
        """Parse the value of the metafield based on the :attr:`type`
        property.
        """
        value: Any
        if self.type == 'json_string':
            value = json.loads(self.value)
        elif self.type == 'single_line_text_field':
            value = self.value
        else:
            raise NotImplementedError(self.type)
        return parser(value)