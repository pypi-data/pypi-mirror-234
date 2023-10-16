#!/usr/bin/env python
# *****************************************************************************
# Copyright (C) 2023 Thomas Touhey <thomas@touhey.fr>
#
# This software is governed by the CeCILL 2.1 license under French law and
# abiding by the rules of distribution of free software. You can use, modify
# and/or redistribute the software under the terms of the CeCILL 2.1 license as
# circulated by CEA, CNRS and INRIA at the following URL: https://cecill.info
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL 2.1 license and that you accept its terms.
# *****************************************************************************
"""Utilities for the TeaL web listener."""

from __future__ import annotations

import json
import re
from base64 import b64decode, b64encode
from datetime import datetime
from logging import getLogger
from typing import ClassVar, TypeVar
from urllib.parse import parse_qsl, urlencode, urlparse

from fastapi import FastAPI, Request
from pydantic import BaseModel, Extra, Field
from pydantic.networks import AnyHttpUrl
from starlette.types import Receive, Scope, Send

from teal.amq import PowensHMACSignature
from teal.redis import get_stored_state

from .config import Settings
from .exceptions import (
    EmptyStateException, MissingStateException, PowensWebhookClientException,
    UnknownStateException,
)

__all__ = [
    'Base64JSONEncodedCallbackState',
    'CallbackStateInformation',
    'OpenIDCIBAPingPayload',
    'OpenIDCIBAPushErrorPayload',
    'OpenIDCIBAPushTokenPayload',
    'PowensPackedCallbackState',
    'QueryStringMiddleware',
    'find_state_in_url',
    'fix_url_query_separator',
    'get_powens_hmac_signature',
    'get_powens_user_token',
]

logger = getLogger(__name__)

Base64JSONEncodedCallbackStateType = TypeVar(
    'Base64JSONEncodedCallbackStateType',
    bound='Base64JSONEncodedCallbackState',
)

CallbackStateInformationType = TypeVar(
    'CallbackStateInformationType',
    bound='CallbackStateInformation',
)

PowensPackedCallbackStateType = TypeVar(
    'PowensPackedCallbackStateType',
    bound='PowensPackedCallbackState',
)


class QueryStringMiddleware:
    """Middleware for supporting URLs with a different query string marker.

    This is useful for APIs with weird query string management, such as
    ``https://example.org/callback&state=abc&code=def``, where the query string
    is actually marked with a first ampersand rather than a question mark.
    """

    __slots__ = ('app', 'delimiter')

    app: FastAPI
    """The application on which the middleware should act."""

    delimiter: str
    """The delimiter used as an alternative to ``?``.

    For example, if using ``&`` as the delimiter here, the query string
    determined from the ``https://example.org/callback&state=abc&code=def``
    will be ``state=abc&code=def``.
    """

    def __init__(self, app: FastAPI, *, delimiter: str):
        self.app = app
        self.delimiter = delimiter

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """Process a request with the query string middleware."""
        if scope['type'] == 'http':
            path = scope['path']
            qs = scope['query_string']
            if not qs and self.delimiter in path:
                path, _, qs = path.partition(self.delimiter)
                scope['path'] = path
                scope['query_string'] = qs.encode('utf-8')

        await self.app(scope, receive, send)


class OpenIDCIBAPingPayload(BaseModel):
    """OpenID Connect CIBA Ping payload.

    This model is taken from `OpenID Connect Client-Initiated Backchannel
    Authentication Flow`_ (Core 1.0) specification, section 10.2.

    .. _`OpenID Connect Client-Initiated Backchannel Authentication Flow`:
        https://openid.net/specs
        /openid-client-initiated-backchannel-authentication-core-1_0.html
    """

    class Config:
        """Model configuration."""

        extra = Extra.forbid

    auth_req_id: str
    """The authentication request identifier."""


class OpenIDCIBAPushTokenPayload(BaseModel):
    """OpenID Connect CIBA Push Successful Token payload.

    This model is taken from `OpenID Connect Client-Initiated Backchannel
    Authentication Flow`_ (Core 1.0) specification, section 10.3.1.

    .. _`OpenID Connect Client-Initiated Backchannel Authentication Flow`:
        https://openid.net/specs
        /openid-client-initiated-backchannel-authentication-core-1_0.html
    """

    class Config:
        """Model configuration."""

        extra = Extra.forbid

    auth_req_id: str
    """The authentication request identifier."""

    access_token: str
    """The obtained access token."""

    token_type: str
    """The token type."""

    refresh_token: str
    """The refresh token."""

    expires_in: int
    """The number of seconds in which the token expires."""

    id_token: str
    """The OpenID token."""


class OpenIDCIBAPushErrorPayload(BaseModel):
    """OpenID Connect CIBA Push Error payload.

    This model is taken from `OpenID Connect Client-Initiated Backchannel
    Authentication Flow`_ (Core 1.0) specification, section 12.

    .. _`OpenID Connect Client-Initiated Backchannel Authentication Flow`:
        https://openid.net/specs
        /openid-client-initiated-backchannel-authentication-core-1_0.html
    """

    class Config:
        """Model configuration."""

        extra = Extra.forbid

    auth_req_id: str
    """The authentication request identifier."""

    error: str
    """The error code, usually among:

    ``access_denied``
        The end-user denied the authorization request.

    ``expired_token``
        The authentication request identifier has expired. The Client will need
        to make a new Authentication Request.

    ``transaction_failed``
        The OpenID Provider encountered an unexpected condition that prevented
        it from successfully completing the transaction.
    """

    error_description: str | None = None
    """The human-readable text providing additional information."""


class Base64JSONEncodedCallbackState(BaseModel):
    """Base64-encoded JSON callback state handling.

    Such states mainly use the TeaL Web Listener as a bouncer.
    They are base64-encoded UTF-8 JSON payloads with the following keys:

    * ``redirect_uri``: The final redirect URL.
    * ``state``: The state to include in the final redirect URL.

    Note that while the initially encoded state may have had base64 padding,
    they may have been trimmed by authorization servers through which the
    state has transited, and as such, we must support this case as well.
    """

    final_redirect_url: AnyHttpUrl
    """The final redirect URL."""

    def encode(self, /) -> str:
        """Encode the state into a base64 JSON-encoded callback state.

        :return: The encoded version of the state information.
        """
        parsed_url = urlparse(self.final_redirect_url)
        query_params = dict(parse_qsl(
            parsed_url.query,
            keep_blank_values=True,
        ))

        if query_params and set(query_params) != {'state'}:
            raise ValueError(
                'Unencodable set of query parameters: '
                + ', '.join(sorted(query_params)),
            )

        data = {'redirect_uri': parsed_url._replace(query=None).geturl()}
        if 'state' in query_params:
            data['state'] = query_params['state']

        return b64encode(
            json.dumps(data, separators=(',', ':')).encode('utf-8'),
        ).decode('utf-8')

    @classmethod
    def decode(
        cls: type[Base64JSONEncodedCallbackStateType],
        value: str,
        /,
    ) -> Base64JSONEncodedCallbackStateType:
        """Decode a base64 JSON encoded callback state.

        :param value: The raw value to decode.
        :return: The decoded state.
        :raises ValueError: An invalid format was detected.
        """
        try:
            data = json.loads(b64decode(value + '===').decode('utf-8'))
        except ValueError as exc:
            raise ValueError('Invalid format') from exc

        try:
            final_redirect_url = data['redirect_uri']
        except KeyError as exc:
            raise ValueError(
                'Missing "redirect_uri" key in encoded JSON',
            ) from exc

        if 'state' in data:
            parsed_url = urlparse(data['redirect_uri'])
            query_params = dict(parse_qsl(
                parsed_url.query,
                keep_blank_values=True,
            ))
            query_params['state'] = data['state']

            final_redirect_url = parsed_url._replace(
                query=urlencode(query_params),
            ).geturl()

        return cls(final_redirect_url=final_redirect_url)


class PowensPackedCallbackState(BaseModel):
    """Packed callback state format handler from Powens.

    The format for the state is the following::

        B1<config flags>[port]<host suffix><path index><host>[_<state>]

    Where:

    * The configuration flags are represented as a single character encoded
      unsigned integer (up to 63), with each bit representing a flag.
    * (only present if ``PORT_SET`` flag is set) The port, as a
      three-character (18-bit) big-endian encoded value for the port.
    * The host suffix, as a one-character integer.
    * The path code, as a one-character integer.
    * The host, stripped of its suffix.
    * The state to provide to the final URL.

    Note that if there is no state to transmit, the underscore does not need
    to be present.

    The allowed configuration flags are the following:

    * ``PORT_SET`` (0x01): whether the port is the non-standard port for
      the provided protocol.
    * ``PORT_DEFAULT`` (0x02): whether the non-standard port is the default
      non-standard port 3158 (1) or is provided in the three characters
      following the configuration flags. This flag is a no-op if
      ``PORT_SET`` is not set.
    * ``HAS_FRAGMENT`` (0x04): whether the fragment should be forcefully
      gathered by the callback.
    * ``IS_HTTP`` (0x08): whether the protocol of the final redirect is
      'http' (1) or 'https' (0).

    Other configuration flags (0x10, 0x20) are reserved and should be set to 0.

    Example packed URL states are the following:

    ``B1001www.example.org``
        Redirect to ``https://www.example.org/`` (no port, no fragment,
        use HTTPS, empty host suffix, ``/`` path).

    ``B1021budgea_abc``
        Redirect to ``https://budgea-sandbox.biapi.pro/?state=abc`` (no port,
        no fragment, use HTTPS, ``-sandbox.biapi.pro`` host suffix,
        ``/`` path).

    ``B1033budgea``
        Redirect to ``https://budgea.biapi.pro/2.0/webauth/resume``
        (no port, no fragment, use HTTPS, ``.biapi.pro`` host suffix,
        ``/2.0/webauth/resume`` path).

    ``B1b02localhost``
        Redirect to ``http://localhost:3158/webauth/resume``
        (port set to default non-standard port 3158, use HTTP, empty host
        suffix, ``/webauth/resume`` path).

    ``B110ji01localhost``
        Redirect to ``https://localhost:1234/`` (port set to non-standard port
        1234, use HTTPS, empty host suffix, ``/`` path).

        Note that ``0ji`` is the encoded version of 1234, since:

        * The offset of ``i`` is 18.
        * The offset of ``j`` is 19.
        * The offset of ``0`` is 0.
        * The result of ``0 * 64 ** 2 + 19 * 64 + 18`` is 1234.
    """

    PORT_SET: ClassVar[int] = 0x01
    """Flag set when the port is the non-standard port for the scheme."""

    PORT_DEFAULT: ClassVar[int] = 0x03
    """Flag set when the port is the default non-standard port 3158.

    Note that this is a combination of 0x01 and 0x02, as 0x02 on its own
    is ineffective.
    """

    HAS_FRAGMENT: ClassVar[int] = 0x04
    """Flag set when the fragment should systematically be gathered."""

    IS_HTTP: ClassVar[int] = 0x08
    """Flag set when the scheme is 'http' instead of 'https'."""

    CHARACTER_SET: ClassVar[str] = (
        '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-.'
    )
    """Characters served for encoding an integer.

    Note that this set is 64-characters long, which means an integer encoded
    using this character set is 6-bit wide (0 to 63).
    """

    DEFAULT_NONSTANDARD_PORT: ClassVar[int] = 3158
    """Default port."""

    DECODE_PATTERN: ClassVar[re.Pattern] = re.compile(
        r'B1(?:([159dhlptxBFJNRVZ])([^_]{3})|([^159dhlptxBFJNRVZ]))'
        + r'([^_])([^_])([^_]+)(?:_(.*))?',
    )
    """The pattern for decoding the state.

    Note that ``159dhlptxBFJNRVZ`` includes all of the characters for which
    ``PORT_SET`` is set but ``PORT_DEFAULT`` is unset, which constitutes the
    condition in which the port is present.
    """

    KNOWN_HOST_SUFFIXES: ClassVar[dict[int, str]] = {
        0: '',
        2: '-sandbox.biapi.pro',
        3: '.biapi.pro',
    }
    """Known host endings."""

    KNOWN_PATHS: ClassVar[dict[int, str]] = {
        1: '/',
        2: '/webauth/resume',
        3: '/2.0/webauth/resume',
    }
    """Known path prefixes."""

    final_redirect_url: AnyHttpUrl
    """The final redirect URL."""

    with_fragment: bool = False
    """Whether to force gathering fragments for the provided state."""

    def encode(self, /) -> str:
        """Encode the state data into the packed URL state format.

        :return: The encoded version of the stored state information.
        :raises ValueError: The data from the URL state is invalid.
        """
        parsed_url = urlparse(self.final_redirect_url)

        config_flags = 0
        if self.with_fragment:
            config_flags |= self.HAS_FRAGMENT

        # Prepare the scheme.
        scheme = parsed_url.scheme.casefold()
        if scheme == 'http':
            config_flags |= self.IS_HTTP

        # Prepare the port flags and encoded extension, if relevant.
        port = (
            parsed_url.port if parsed_url.port is not None
            else 80 if scheme == 'http'
            else 443
        )

        if (
            (scheme == 'http' and port == 80)
            or (scheme == 'https' and port == 443)
        ):
            encoded_port = ''
        elif port == self.DEFAULT_NONSTANDARD_PORT:
            config_flags |= self.PORT_DEFAULT
            encoded_port = ''
        else:
            config_flags |= self.PORT_SET
            encoded_port = (
                self.CHARACTER_SET[(port >> 12) & 63]
                + self.CHARACTER_SET[(port >> 6) & 63]
                + self.CHARACTER_SET[port & 63]
            )

        # Find the largest host suffix index that matches our host.
        host = parsed_url.hostname or ''
        host_suffix_index, host_suffix_length = max(
            (
                (index, len(suffix))
                for index, suffix in self.KNOWN_HOST_SUFFIXES.items()
                if host.endswith(suffix) and host != suffix
            ),
            key=lambda x: x[1],
        )

        # Check that the host is indeed encodable.
        if host_suffix_length > 0:
            host = host[:-host_suffix_length]

        invalid_chars = set(
            c for c in host
            if c not in self.CHARACTER_SET
        )
        if invalid_chars:
            raise ValueError(
                'Unencodable characters in hostname before prefix: '
                + ''.join(sorted(invalid_chars)),
            )

        # Find the path index that matches our path.
        path = parsed_url.path or '/'
        for index, value in self.KNOWN_PATHS.items():
            if path == value:
                path_index = index
                break
        else:
            raise ValueError(f'Unencodable path {path!r}')

        # Extract the state suffix if necessary.
        query_params = dict(parse_qsl(
            parsed_url.query,
            keep_blank_values=True,
        ))
        if not query_params:
            state_suffix = ''
        elif set(query_params) == {'state'}:
            state = query_params['state']
            invalid_chars = set(
                c for c in state
                if c not in self.CHARACTER_SET + '_'
            )
            if invalid_chars:
                raise ValueError(
                    'Unencodable characters in state: '
                    + ''.join(sorted(invalid_chars)),
                )

            state_suffix = '_' + state
        else:
            raise ValueError(
                'Unencodable set of query parameters: '
                + ', '.join(sorted(query_params)),
            )

        return (
            'B1'
            + self.CHARACTER_SET[config_flags]
            + encoded_port
            + self.CHARACTER_SET[host_suffix_index]
            + self.CHARACTER_SET[path_index]
            + host
            + state_suffix
        )

    @classmethod
    def decode(
        cls: type[PowensPackedCallbackStateType],
        value: str,
        /,
    ) -> PowensPackedCallbackStateType:
        """Decode a packed URL state type.

        :param value: The raw value to decode.
        :return: The state to decode.
        :raises ValueError: An invalid format was detected.
        """
        invalid_chars = set(
            c for c in value
            if c not in cls.CHARACTER_SET + '_'
        )
        if invalid_chars:
            raise ValueError(
                'Invalid characters in the input: '
                + ''.join(sorted(invalid_chars)),
            )

        match = cls.DECODE_PATTERN.fullmatch(value)
        if match is None:
            raise ValueError('Invalid format in the input.')

        config_flags = cls.CHARACTER_SET.find(match.group(1) or match.group(3))
        if config_flags & 0x30:
            raise ValueError(
                f'Unsupported flag set: 0x{config_flags & 0x30:02x}',
            )

        host_suffix_index = cls.CHARACTER_SET.find(match.group(4))
        try:
            host_suffix = cls.KNOWN_HOST_SUFFIXES[host_suffix_index]
        except KeyError as exc:
            raise ValueError(
                f'Invalid host suffix index {host_suffix_index}',
            ) from exc

        path_index = cls.CHARACTER_SET.find(match.group(5))
        try:
            path = cls.KNOWN_PATHS[path_index]
        except KeyError as exc:
            raise ValueError(
                f'Invalid path index {path_index}',
            ) from exc

        raw_port = match.group(2) or ''
        port: int | None = None
        if raw_port:
            port = (
                cls.CHARACTER_SET.find(raw_port[0]) * 4096
                + cls.CHARACTER_SET.find(raw_port[1]) * 64
                + cls.CHARACTER_SET.find(raw_port[2])
            )
        elif config_flags & cls.PORT_DEFAULT == cls.PORT_DEFAULT:
            port = cls.DEFAULT_NONSTANDARD_PORT

        if (
            (port == 80 and config_flags & cls.IS_HTTP)
            or (port == 443 and ~config_flags & cls.IS_HTTP)
        ):
            port = None

        scheme = 'http' if config_flags & cls.IS_HTTP else 'https'
        host = match.group(6) + host_suffix
        if port is not None:
            host += f':{port}'

        query_string = ''
        raw_state = match.group(7)
        if raw_state is not None:
            query_string += f'?state={raw_state}'

        return cls(
            final_redirect_url=f'{scheme}://{host}{path}{query_string}',
            with_fragment=bool(config_flags & cls.HAS_FRAGMENT),
        )


class CallbackStateInformation(BaseModel):
    """State information, to be exploited in the router."""

    state: str = Field(min_length=1)
    """The callback state."""

    final_redirect_url: AnyHttpUrl | None = None
    """The final redirect URL."""

    with_fragment: bool = False
    """Whether to force gathering the fragment or not."""

    @classmethod
    def from_powens_redirect_data(
        cls: type[CallbackStateInformationType],
        /,
        *,
        state: str,
        final_redirect_url: str,
        with_fragment: bool = False,
        full_url: str,
        request: Request,
    ) -> CallbackStateInformationType:
        """Get callback state information from redirect data.

        :param state: The state for which to redirect.
        :param final_redirect_url: The final redirect URL to redirect to.
        :param with_fragment: Whether to force getting the fragment or not.
        :param full_url: The full URL from which to gather the original
            parameters.
        :param request: The request in which the callback URL was submitted.
        """
        parsed_callback_url = urlparse(full_url)
        callback_query_params = dict(parse_qsl(
            parsed_callback_url.query,
            keep_blank_values=True,
        ))

        parsed_final_redirect_url = urlparse(final_redirect_url)
        final_query_params = dict(parse_qsl(
            parsed_final_redirect_url.query,
            keep_blank_values=True,
        ))

        if 'state' in callback_query_params:
            # If no final state has been provided, we do not want to transmit
            # the state from the listener's callback URL.
            del callback_query_params['state']

        # We can now add the query parameters from the final redirect URL.
        callback_query_params.update(final_query_params)

        # We try to determine whether we're in an app-to-app or pure web flow.
        if request.headers.get('Referer'):
            callback_query_params['auth_type'] = 'web'
        else:
            callback_query_params['auth_type'] = 'app'

        final_redirect_url = parsed_final_redirect_url._replace(
            query=urlencode(callback_query_params),
        ).geturl()

        return cls(
            state=state,
            final_redirect_url=final_redirect_url,
            with_fragment=with_fragment,
        )

    @classmethod
    async def from_url(
        cls: type[CallbackStateInformationType],
        full_url: str,
        /,
        *,
        request: Request,
        settings: Settings,
    ) -> CallbackStateInformationType:
        """Get state information regarding a state provided in an URL.

        :param full_url: The full URL from which to gather a state.
        :param settings: The settings applying to the current request.
        :return: The callback information obtained from the state present
            in the callback URL.
        :raises MissingStateException: No callback state could be found.
        :raises EmptyStateException: The found callback state was empty.
        :raises UnknownStateException: No callback state information could
            be retrieved using the found callback state.
        """
        state = find_state_in_url(full_url)
        if state is None:
            logger.info('No state found in URL: %s', full_url)
            raise MissingStateException()

        if state == '':
            logger.info('Found state was empty in URL: %s', full_url)
            raise EmptyStateException()

        stored_state = await get_stored_state(state, settings=settings)
        if stored_state is not None:
            # Logging for this case is done in ``get_stored_state`` directly.
            return cls(
                state=state,
                final_redirect_url=stored_state.final_redirect_url,
                with_fragment=stored_state.with_fragment,
            )

        if settings.powens_redirect_fallback:
            try:
                obj = Base64JSONEncodedCallbackState.decode(state)
            except ValueError as exc:
                logger.debug(
                    'Could not decode the state as a base64-encoded JSON '
                    + 'bouncer state: %s',
                    exc,
                )
            else:
                logger.info(
                    'Decoded the state as a base64-encoded JSON bouncer '
                    + 'state.',
                )
                return cls.from_powens_redirect_data(
                    state=state,
                    final_redirect_url=obj.final_redirect_url,
                    full_url=full_url,
                    request=request,
                )

            try:
                obj = PowensPackedCallbackState.decode(state)
            except ValueError as exc:
                logger.debug(
                    'Could not decode the state as a Powens packed callback '
                    + 'state: %s',
                    exc,
                )
            else:
                logger.info(
                    'Decoded the state as a Powens packed callback state.',
                )
                return cls.from_powens_redirect_data(
                    state=state,
                    final_redirect_url=obj.final_redirect_url,
                    with_fragment=obj.with_fragment,
                    full_url=full_url,
                    request=request,
                )

        logger.info(
            'No callback data could be determined from state "%s".',
            state,
        )
        raise UnknownStateException()


def fix_url_query_separator(url: str, /) -> str:
    """Replace alternative query separators with '?' if necessary.

    This helps mirroring the behaviour we have with
    :py:class:`QueryStringMiddleware` with the ``/raw-callback``
    ASGI endpoint.

    :param url: The URL to fix.
    :return: The fixed URL.
    """
    parsed_url = urlparse(url)

    if not parsed_url.query and '&' in parsed_url.path:
        path, _, query = parsed_url.path.partition('&')
        parsed_url = parsed_url._replace(
            path=path,
            query=query,
        )

    return parsed_url.geturl()


def find_state_in_url(url: str, /) -> str | None:
    """Find the state in a given URL.

    Note that this will look for query parameters first, then fragment
    if necessary.

    :param url: The URL to look for a state in.
    :return: The found state, or None if no state could be found.
    """
    parsed_url = urlparse(url)

    # The state might be in the full URL query parameters.
    params = dict(parse_qsl(parsed_url.query, keep_blank_values=True))
    if 'state' in params:
        return params['state']

    # We suppose the fragment is formatted like HTTP parameters, so we
    # want to use this hypothesis to try and get a 'state' in the
    # fragment.
    params = dict(parse_qsl(
        parsed_url.fragment,
        keep_blank_values=True,
    ))
    return params.get('state')


def get_powens_user_token(request: Request) -> str | None:
    """Get the Powens user-scoped token if available.

    For more information, see `Authentication with user-scoped token`_.

    :param request: The request from which to gather a user-scoped token.
    :return: The user-scoped token, or None if no such token could be found.

    .. _`Authentication with user-scoped token`:
        https://docs.powens.com/documentation/integration-guides/webhooks
        #authentication-with-user-scoped-token
    """
    try:
        authorization = request.headers['Authorization']
    except KeyError:
        return None

    auth_type, _, auth_data = authorization.partition(' ')
    if auth_type.casefold() != 'bearer':
        raise PowensWebhookClientException(
            detail=f'Unhandled authorization type {auth_type!r}',
        )

    if not auth_data:
        raise PowensWebhookClientException(detail='Missing user-scoped token')

    return auth_data


def get_powens_hmac_signature(request: Request) -> PowensHMACSignature | None:
    """Get the Powens HMAC signature from a fastapi request.

    For more information on the expected headers or header format, see
    `Authentication with a HMAC signature header`_.

    :param request: The request from which to gather the HMAC signature data.
    :return: The HMAC signature, or None if no such signature could be found.

    .. _`Authentication with a HMAC signature header`:
        https://docs.powens.com/documentation/integration-guides/webhooks
        #authentication-with-a-hmac-signature-header
    """
    try:
        signature = request.headers['BI-Signature']
    except KeyError:
        return None

    try:
        raw_signature_date = request.headers['BI-Signature-Date']
    except KeyError:
        raise PowensWebhookClientException(detail='Missing signature date')

    try:
        # Check that the signature is indeed correctly base64 encoded.
        b64decode(signature, validate=True)
    except ValueError:
        raise PowensWebhookClientException(
            detail='Signature is not valid base64',
        )

    try:
        adapted_raw_signature_date = raw_signature_date
        if adapted_raw_signature_date.endswith('Z'):
            adapted_raw_signature_date = (
                adapted_raw_signature_date[:-1] + '+00:00'
            )

        signature_date = datetime.fromisoformat(adapted_raw_signature_date)
    except ValueError:
        raise PowensWebhookClientException(
            detail='Signature date is not ISO formatted',
        )

    if signature_date.tzinfo is None:
        raise PowensWebhookClientException(
            detail='Signature date is missing a timezone',
        )

    # Signature prefix is the following:
    # <METHOD> + "." + <ENDPOINT> + "." + <DATE> + "." + <PAYLOAD>
    payload_prefix = (
        f'{request.method.upper()}.{request.url.path}.{raw_signature_date}.'
    )

    return PowensHMACSignature(
        signature=signature,
        payload_prefix=payload_prefix,
        signature_date=signature_date,
    )
