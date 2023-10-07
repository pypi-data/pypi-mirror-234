# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .basicauth import BasicAuth
from .connecttimeout import ConnectTimeout
from .headers import Headers
from .ibackoff import IBackoff
from .iclient import IClient
from .icredential import ICredential
from .iencrypter import IEncrypter
from .iproductcatalog import IProductCatalog
from .iresponse import IResponse
from .iresponsecache import IResponseCache
from .iresource import IResource
from .iresourcemeta import IResourceMeta
from .irequest import IRequest
from .nullbackoff import NullBackoff
from .nullcredential import NullCredential
from .optionsresponse import OptionsResponse
from .ratelimited import RateLimited
from .hints import RequestContent
from .readtimeout import ReadTimeout
from .resourcedoesnotexist import ResourceDoesNotExist
from .resourcexception import ResourceException
from .resourcexceptiontype import ResourceExceptionType
from .serverdoesnotexist import ServerDoesNotExist
from .wwwauthenticateheader import WWWAuthenticateHeader


__all__: list[str] = [
    'BasicAuth',
    'ConnectTimeout',
    'Headers',
    'IBackoff',
    'IClient',
    'ICredential',
    'IEncrypter',
    'IProductCatalog',
    'IResource',
    'IResourceMeta',
    'IResponse',
    'IResponseCache',
    'IRequest',
    'NullBackoff',
    'NullCredential',
    'OptionsResponse',
    'RateLimited',
    'ReadTimeout',
    'RequestContent',
    'ResourceDoesNotExist',
    'ResourceException',
    'ResourceExceptionType',
    'ServerDoesNotExist',
    'WWWAuthenticateHeader'
]