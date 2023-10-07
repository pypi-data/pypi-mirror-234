# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from typing import TypeVar

from ckms.core import parse_dsn
from ckms.core import parse_spec

from .client import Client


T = TypeVar('T', bound=Client)


class ApplicationClient(Client):
    """A :class:`headless.ext.oauth2.Client` implementation that retrieves
    the credentials from environment variables. Supports the following
    client authentication methods:
    
    - ``private_key_jwt``
    
    """
    __module__: str = 'headless.ext.oauth2'

    @classmethod
    def fromenv(
        cls: type[T],
        issuer: str
    ) -> T:
        """Create a new :class:`ApplicationClient` from well-known
        environment variables.
        
        Args:
            issuer (str): points to the authorization server to create a
                client for. Must expose an :rfc:`8414` compliant metadata
                endpoint. If the authorization server does not expose
                such an endpoint, the `token_endpoint` parameter is required.
            token_endpoint (str): the :term:`Token Endpoint` of the authorization
                server, if it does not support autodiscovery using an :rfc:`8414`
                metadata endpoint.

        Returns:
            ApplicationClient
        """
        if not os.getenv('APP_CLIENT_ID'):
            raise ValueError("Provide the APP_CLIENT_ID environment variable.")
        if not os.getenv('APP_SIGNING_KEY'):
            raise ValueError("Provide the APP_SIGNING_KEY environment variable.")
        if not os.getenv('APP_ENCRYPTION_KEY'):
            raise ValueError("Provide the APP_ENCRYPTION_KEY environment variable.")
        return cls(
            client_id=os.environ['APP_CLIENT_ID'],
            issuer=issuer,
            signing_key=parse_spec(parse_dsn(os.environ['APP_SIGNING_KEY'])),
            encryption_key=parse_spec(parse_dsn(os.environ['APP_ENCRYPTION_KEY']))
        )