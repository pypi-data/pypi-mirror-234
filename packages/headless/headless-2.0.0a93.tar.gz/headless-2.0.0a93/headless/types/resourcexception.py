# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

from .iresponse import IResponse
from .iresource import IResource


T = TypeVar('T', bound='ResourceException')


class ResourceException(BaseException):
    __abstract__: bool = True
    __module__: str = 'headless.types'
    model: type[IResource]
    response: IResponse[Any, Any]

    def __init__(
        self,
        model: type[IResource],
        response: IResponse[Any, Any]
    ) -> None:
        self.model = model
        self.response = response