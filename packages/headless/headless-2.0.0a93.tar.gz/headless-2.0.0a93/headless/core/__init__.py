# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .basecredential import BaseCredential
from .baserotatingcredential import BaseRotatingCredential
from .basicauthcredential import BasicAuthCredential
from .baseinventorycatalog import BaseInventoryCatalog
from .deferredresource import DeferredResource
from .diskresponsecache import DiskResponseCache
from .linearbackoff import LinearBackoff
from .nullresponsecache import NullResponseCache
from .resource import Resource # type: ignore
from .resourcemeta import ResourceMeta
from .resourcemetaclass import ResourceMetaclass
from .resourcereference import ResourceReference


__all__: list[str] = [
    'BaseCredential',
    'BaseRotatingCredential',
    'BasicAuthCredential',
    'BaseInventoryCatalog',
    'DeferredResource',
    'DiskResponseCache',
    'LinearBackoff',
    'NullResponseCache',
    'Resource',
    'ResourceMeta',
    'ResourceMetaclass',
    'ResourceReference',
]


def Reference(model: type[Resource], attname: str) -> Any:
    return ResourceReference(model, attname)