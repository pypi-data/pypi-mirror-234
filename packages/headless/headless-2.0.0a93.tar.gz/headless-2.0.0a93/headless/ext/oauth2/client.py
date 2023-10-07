# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import binascii
import copy
import functools
import logging
import urllib.parse
from typing import Any
from typing import NoReturn

from ckms.core import Keychain
from ckms.core import KeySpecification
from ckms.core.models import JOSEObject
from ckms.core.models import JSONWebSignature
from ckms.types import Algorithm
from ckms.types import JSONWebKeySet
from ckms.types import Malformed
from ckms.types import InvalidSignature
from ckms.types import KeyOperationType
from ckms.types import KeyUseType
from ckms.types.invalidtoken import InvalidToken

from headless.core import httpx
from headless.types import IResponse
from .clientcredential import ClientCredential
from .models import AuthorizationCode
from .models import ClaimSet
from .models import ClientAuthenticationMethod
from .models import ClientCredentialsRequest
from .models import Error
from .models import IObtainable
from .models import OIDCToken
from .models import TokenResponse
from .models import ServerMetadata
from .nullcredential import NullCredential
from .nullclientstorage import NullClientStorage
from .server import Server
from .types import ResponseIntegrityError
from .types import IClientStorage
from .types import RefreshTokenException



JWKS_CACHE: dict[str, JSONWebKeySet] = {}
keychain: Keychain = Keychain()


class Client(httpx.Client):
    """A :class:`headless.core.httpx.Client` implementation for use with
    Open Authorization/OpenID Connect servers.
    """
    __module__: str = 'headless.ext.oauth2'
    credential: ClientCredential
    jwks: JSONWebKeySet | None = None
    logger: logging.Logger = logging.getLogger('headless.ext.oauth2')
    scope: set[str]
    storage: IClientStorage
    trust_email: bool

    @property
    def client_id(self) -> str | None:
        return self.credential.client_id

    @property
    def metadata(self) -> ServerMetadata:
        assert self.server.metadata is not None
        return self.server.metadata

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        issuer: str | None = None,
        storage: IClientStorage = NullClientStorage(),
        client_auth: ClientAuthenticationMethod | None = None,
        authorization_endpoint: str | None = None,
        token_endpoint: str | None = None,
        trust_email: bool = False,
        scope: set[str] | None = None,
        params: dict[str, str] | None = None,
        signing_key: KeySpecification | None = None,
        encryption_key: KeySpecification | None = None,
        **kwargs: Any
    ):
        self.server = Server(
            client=self,
            autodiscover=bool(issuer),
            authorization_endpoint=authorization_endpoint,
            token_endpoint=token_endpoint,
            **kwargs
        )
        self.params = params
        self.storage = storage
        self.scope = set(scope or set())
        self.trust_email = trust_email

        # Add the signing key and encryption key to the keychain.
        if signing_key and client_id and not keychain.has(f'{client_id}/sig'):
            keychain.add(f'{client_id}/sig', signing_key)

        # If the client_id is None, then this client is configured for
        # a limited set of operations such as discovery, userinfo, etc.
        if client_id is None:
            credential = NullCredential()
        else:
            credential=ClientCredential(
                client_id=client_id,
                client_secret=client_secret,
                keychain=keychain,
                server=self.server,
                using=client_auth
            )
        super().__init__(base_url=issuer or '', credential=credential, **kwargs)

    def get_client_id(self) -> str:
        if not self.client_id:
            raise ValueError("Client is configured for metadata only.")
        return self.client_id

    def get_issuer(self) -> str:
        """Get the issuer identifier of the authorization server."""
        # If server is autodiscovered, return the 'iss' claim from the
        # metadata, else derive if from the token endpoint.
        issuer = None
        if self.server.metadata is not None:
            issuer = self.server.metadata.issuer
        if issuer is None:
            assert self.server.token_endpoint is not None
            p = urllib.parse.urlparse(self.server.token_endpoint)
            issuer = f'{p.scheme}://{p.netloc}'
        return issuer

    def get_token_endpoint(self) -> str:
        if not self.server.token_endpoint:
            raise ValueError("Token endpoint was not discovered.")
        return self.server.token_endpoint

    # REFACTOR
    async def authorize(
        self,
        state: str,
        redirect_uri: str | None,
        scope: set[str] | None = None,
        nonce: str | None = None,
        resources: set[str] | None = None,
        **extra: Any
    ) -> str:
        """Create an authorization request and return the URI to which
        the resource owner must be redirected.

        The `state` parameter is mandatory and is used to correlate the
        redirect to a specific authorization request.

        The `redirect_uri` parameter *might* be optional depending on the
        OAuth 2.x server. If the server does not allow omitting the
        `redirect_uri` parameter, this argument is mandatory.
        """
        scope = set(scope or []) | self.scope
        if nonce is not None:
            scope.update({'openid'})
            extra.update({'nonce': nonce})
        url=self.server.authorization_endpoint
        params: dict[str, str] = {
            **extra,
            'client_id': self.credential.client_id,
            'state': state,
            'response_type': 'code',
        }
        if redirect_uri is not None:
            params['redirect_uri'] = redirect_uri
        if scope:
            params['scope'] = str.join(' ', sorted(scope))

        if self.params is not None:
            params.update(copy.deepcopy(self.params))

        # Convert the parameters to a list of tuples, as some parameters
        # need to be repeated.
        query: list[tuple[str, str]] = list(params.items())
        for resource in (resources or []):
            query.append(('resource', resource))

        # We encode the URL because some libraries use plus
        # encoding.
        url += '?' + urllib.parse.urlencode(query, quote_via=urllib.parse.quote)
        return url

    async def client_credentials(
        self,
        scope: set[str] | str,
        resource: str | None = None
    ) -> TokenResponse:
        """Obtain an access token using the configured client."""
        if self.client_id is None:
            raise ValueError(
                "Only confidential (authenticated) clients may use the "
                "client_credentials grant."
            )
        if not isinstance(scope, str):
            scope = str.join(' ', sorted(scope))
        return await self.token(ClientCredentialsRequest(
            client_id=self.client_id,
            resource=resource,
            scope=scope
        ))

    async def discover(self) -> None:
        await self.server.discover()

    @functools.singledispatchmethod
    async def token(
        self,
        obj: Any,
        **kwargs: Any
    ) -> TokenResponse:
        """Obtain an access token using the given grant."""
        if not isinstance(obj, IObtainable) or self.server.metadata is None:
            raise NotImplementedError
        return await obj.obtain(self, self.server.metadata)

    @token.register
    async def exchange_authorization_code(
        self,
        dto: AuthorizationCode,
        redirect_uri: str,
    ) -> TokenResponse:
        params: dict[str, str] = {
            'client_id': self.credential.client_id,
            'code': dto.code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }
        response = await self.post(
            url=self.server.token_endpoint,
            data=params
        )
        response.raise_for_status()
        return TokenResponse.parse_obj(await response.json())

    async def get_server_jwks(self, force_refresh: bool = False) -> JSONWebKeySet:
        assert self.server.metadata is not None
        assert self.server.metadata.issuer is not None
        jwks = self.jwks or JWKS_CACHE.get(self.server.metadata.issuer)
        if jwks is None or force_refresh:
            jwks = JSONWebKeySet()
            if self.metadata.jwks_uri is not None:
                response = await self.get(
                    url=self.metadata.jwks_uri
                )
                if response.status_code != 200:
                    self.logger.critical(
                        "Caught %s response while fetching the server "
                        "JSON Web Keyset. %s.verify() will always return "
                        "False.",
                        response.status_code, type(self).__name__
                    )
                else:
                    jwks = JSONWebKeySet.parse_obj(await response.json())

            # TODO: Some identity providers (Microsoft) omit the key_ops, but
            # as these are public keys we can determine the ops. This code
            # should be moved when CKMS is being rewritten.
            for k in jwks.keys:
                if KeyOperationType.verify in k.key_ops:
                    continue
                if k.use != KeyUseType.sign:
                    continue
                k.key_ops.append(KeyOperationType.verify)

                # Microsoft also omits the alg parameter, so try to retrieve
                # if from the server metadata. If there is more than one we
                # have a problem (TODO).
                supported = self.metadata.id_token_signing_alg_values_supported or []
                if not supported or len(supported) > 1:
                    raise RuntimeError(
                        "Unable to determine the token signing algorithm from the metadata "
                        "and JWKS provided by the authorization server."
                    )
                if k.alg is None:
                    k.alg = Algorithm(supported[0])

            # Add the JSONWebKeySet to the local cache (TODO).
            JWKS_CACHE[self.server.metadata.issuer] = jwks
        return jwks

    async def on_authorize_endpoint_error(
        self,
        response: IResponse[Any, Any]
    ) -> NoReturn:
        response.raise_for_status()
        raise NotImplementedError

    async def on_client_error(
        self,
        response: IResponse[Any, Any]
    ) -> NoReturn | IResponse[Any, Any]:
        try:
            raise Error(**(await response.json()))
        except TypeError:
            pass
        return await super().on_client_error(response)

    async def refresh_token(
        self,
        token: str,
        resource: str | None = None,
        scope: set[str] | None = None
    ) -> TokenResponse:
        """Obtain an access token and a new refresh token."""
        params: dict[str, str] = {
            'grant_type' : 'refresh_token',
            'refresh_token': token
        }
        if resource:
            params['resource'] = resource
        if scope:
            params['scope'] = str.join(' ', sorted(scope))
        response = await self.post(
            url=self.server.token_endpoint,
            data=params
        )
        if response.status_code >= 400:
            raise RefreshTokenException
        response.raise_for_status()
        return TokenResponse.parse_obj(await response.json())

    async def userinfo(self, token: str) -> ClaimSet:
        """Query the OpenID Connect UserInfo endpoint at the authorization
        server using the given `token`.
        """
        if not self.server.userinfo_endpoint:
            raise NotImplementedError(
                f'Authorization server does not expose the '
                'UserInfo endpoint'
            )
        response = await self.get(
            url=self.server.userinfo_endpoint,
            headers={'Authorization': f'Bearer {token}'}
        )
        return ClaimSet.parse_obj(await response.json())

    async def verify_response(
        self,
        response: TokenResponse,
        nonce: str | None = None,
        audience: set[str] | None = None,
        issuer: str | None = None
    ) -> tuple[TokenResponse, OIDCToken | None]:
        """Verifies the response from the authorization servers' token
        endpoint.
        """
        if issuer and issuer != self.issuer:
            raise ResponseIntegrityError(
                "Issuer does not match the expected issuer."
            )
        oidc = None
        if response.id_token:
            oidc = await self.verify_oidc(
                token=response.id_token,
                nonce=nonce,
                audience=audience,
                accept={'jwt'}
            )
            if oidc is None:
                raise ResponseIntegrityError(
                    "Failed verifying OIDC ID Token received from the authorization "
                    "server."
                )
            if oidc.at_hash:
                self.logger.warning("at_hash verification is not implemented.")
            if oidc.c_hash:
                self.logger.warning("c_hash verification is not implemented.")

        return response, oidc

    async def verify_oidc(
        self,
        token :str,
        nonce: str | None = None,
        audience: set[str] | None = None,
        accept: set[str] | None = None,
        verify_azp: bool = True,
    ) -> OIDCToken | None:
        """Return a valid ID Token or None.
        """
        assert self.server.metadata is not None # nosec
        await self.verify(token, nonce=nonce, audience=audience, accept=accept)
        oidc = OIDCToken.parse_jwt(token)
        if oidc.iss != self.metadata.issuer:
            raise ResponseIntegrityError(
                "Issuer does not match the expected issuer."
            )
        if oidc.nonce != nonce:
            self.logger.debug('%s != %s', oidc.nonce, nonce)
            raise ResponseIntegrityError(
                "The nonce in the ID Token does not match the expected nonce."
            )
        if oidc.azp and oidc.azp != self.client_id:
            raise ResponseIntegrityError("Client is not the authorized party.")
        return oidc

    async def verify(
        self,
        token :str,
        nonce: str | None = None,
        audience: set[str] | None = None,
        accept: set[str] | None = None
    ) -> bool:
        """Return a boolean indicating if the token could be verified to
        originate from the configured authorization server.
        """
        assert self.metadata is not None
        accept = accept or {"at+jwt", "jwt"}
        jwks = await self.get_server_jwks()
        try:
            jws = JOSEObject.parse(token)
            if not isinstance(jws, JSONWebSignature):
                raise TypeError
            if jws.typ is not None and str.lower(jws.typ) != 'jwt':
                raise TypeError
            if not await jws.verify(keychain=jwks):
                raise InvalidSignature
            jwt = jws.get_claims()

            # If client_id is None, then were veryfing a token from a
            # third-party (i.e. we are not the client).
            jwt.verify(
                audience={self.client_id} if self.client_id else None,
                issuer=self.metadata.issuer
            )
        except InvalidSignature:
            raise ResponseIntegrityError(
                "The signature in the OIDC ID Token could be verified using the "
                f"known public keys of issuer {self.issuer}"
            )
        except (binascii.Error, Malformed, InvalidSignature, InvalidToken, TypeError):
            return False

        return True
    
    async def verify_signature(self, token: str) -> bool:
        """Verifies that the given token was signed by the authorization
        server.
        """
        jwks = await self.get_server_jwks()
        jws = JOSEObject.parse(token)
        if not isinstance(jws, JSONWebSignature):
            return False
        return await jws.verify(keychain=jwks)

    async def __aenter__(self):
        await super().__aenter__()
        await self.discover()
        return self