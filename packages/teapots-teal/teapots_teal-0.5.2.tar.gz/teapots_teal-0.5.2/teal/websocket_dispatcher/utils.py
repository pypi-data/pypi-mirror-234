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
"""Utilities the TeaL websocket dispatcher."""

from __future__ import annotations

import re
from asyncio import gather as gather_asyncio
from base64 import b64decode
from collections import defaultdict
from contextlib import asynccontextmanager
from logging import getLogger
from typing import Any, AsyncIterator, TypeVar

from fastapi import WebSocket
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser,
)
from starlette.requests import HTTPConnection

from teal.amq import (
    AMQHandler, CallbackMessage, OpenIDCIBACallbackMessage,
    PowensWebhookMessage,
)

from .config import Settings
from .protocol import (
    CallbackServerMessage, OpenIDCIBACallbackServerMessage,
    PowensWebhookServerMessage,
)

__all__ = ['BasicAuthBackend', 'WebsocketDispatcher']

WebsocketDispatcherType = TypeVar(
    'WebsocketDispatcherType',
    bound='WebsocketDispatcher',
)

logger = getLogger(__name__)

HTTP_BASIC_RE = re.compile(r'^Basic ([^\s]+)$')


class BasicAuthBackend(AuthenticationBackend):
    """Basic authentication backend, for decoding HTTP Basic credentials."""

    async def authenticate(
        self,
        conn: HTTPConnection,
    ) -> tuple[AuthCredentials, None]:
        """Authenticate using data present in the connection.

        :param conn: The connection which to read.
        :return: The authentication credentials.
        :raises AuthenticationError: In case of invalid authentication.
        """
        try:
            authorization = conn.headers['Authorization']
        except KeyError:
            # Only if the connection is a websocket, we allow the authorization
            # to be passed through GET parameters.
            if conn.scope['type'] != 'websocket':
                return None, None

            try:
                credentials = conn.query_params['credentials']
            except KeyError:
                return None, None
        else:
            match = HTTP_BASIC_RE.fullmatch(authorization)
            if match is None:
                raise AuthenticationError(
                    'Incorrect HTTP-Basic authorization header',
                )

            credentials = match.group(1)

        try:
            decoded = b64decode(credentials, validate=True).decode('ascii')
            username, separator, password = decoded.partition(':')
            if separator != ':':
                raise ValueError('Missing colon separator')
        except ValueError as exc:
            raise AuthenticationError(
                'Incorrect HTTP-Basic authorization header',
            ) from exc

        settings = Settings()
        if username != 'anonymous' or password != settings.password:
            logger.warning('Invalid credentials')
            raise AuthenticationError('Invalid credentials')

        return AuthCredentials(), SimpleUser(username)


class WebsocketDispatcher:
    """Main class for dispatching websocket event pushes."""

    __slots__ = (
        'amq_handler',
        'callback_state_by_websocket',
        'openid_ciba_request_id_by_websocket',
        'powens_domain_by_websocket',
        'websocket_by_callback_state',
        'websocket_by_openid_ciba_request_id',
        'websocket_by_powens_domain',
    )

    websocket_by_callback_state: defaultdict[str, set[WebSocket]]
    """Set of websockets bound to a particular callback state."""

    callback_state_by_websocket: defaultdict[WebSocket, set[str]]
    """Set of callback states bound to a particular websocket."""

    websocket_by_powens_domain: defaultdict[str, set[WebSocket]]
    """Set of websockets to which the webhooks should be sent for a domain."""

    powens_domain_by_websocket: defaultdict[WebSocket, set[str]]
    """Set of Powens domain whose webhooks are sent to a websocket."""

    websocket_by_openid_ciba_request_id: defaultdict[str, set[WebSocket]]
    """Set of websockets to which the callbacks should be sent for an
    OpenID CIBA callback request identifier.
    """

    openid_ciba_request_id_by_websocket: defaultdict[WebSocket, set[str]]
    """Set of OpenID CIBA callback request identifiers bound for a
    given websocket.
    """

    def __init__(self, /, *, amq_handler: AMQHandler):
        self.amq_handler = amq_handler
        self.websocket_by_callback_state = defaultdict(lambda: set())
        self.callback_state_by_websocket = defaultdict(lambda: set())
        self.websocket_by_powens_domain = defaultdict(lambda: set())
        self.powens_domain_by_websocket = defaultdict(lambda: set())
        self.websocket_by_openid_ciba_request_id = defaultdict(lambda: set())
        self.openid_ciba_request_id_by_websocket = defaultdict(lambda: set())

    @classmethod
    @asynccontextmanager
    async def dispatcher_context(
        cls: type[WebsocketDispatcherType],
        /,
        *,
        settings: Settings,
    ) -> AsyncIterator[WebsocketDispatcherType]:
        """Get a dispatcher in a context.

        :param settings: The settings to use.
        """
        async with AMQHandler.handler_context(
            settings=settings,
        ) as amq_handler:
            dispatcher = cls(amq_handler=amq_handler)
            amq_handler.callback = dispatcher.push
            yield dispatcher

    async def bind_callback_state(
        self, websocket: WebSocket, /, *,
        state: str,
    ) -> None:
        """Bind a websocket to a callback state.

        :param websocket: The websocket to bind.
        :param state: The state to bind to.
        """
        await self.amq_handler.bind_callback_state(state)

        self.websocket_by_callback_state[state].add(websocket)
        self.callback_state_by_websocket[websocket].add(state)

    async def bind_powens_domain(
        self, websocket: WebSocket, /, *,
        domain: str,
    ) -> None:
        """Bind a websocket to Powens webhook calls for a domain.

        :param websocket: The websocket to bind.
        :param domain: The Powens domain to bind for.
        """
        await self.amq_handler.bind_powens_domain_webhooks(domain)

        self.websocket_by_powens_domain[domain].add(websocket)
        self.powens_domain_by_websocket[websocket].add(domain)

    async def bind_openid_ciba_request_identifier(
        self, websocket: WebSocket, /, *,
        request_id: str,
    ) -> None:
        """Bind a websocket to OpenID CIBA callbacks for a request identifier.

        :param websocket: The websocket to bind.
        :param request_id: The request identifier to bind for.
        """
        await self.amq_handler.bind_openid_ciba_request_identifier(request_id)

        self.websocket_by_openid_ciba_request_id[request_id].add(websocket)
        self.openid_ciba_request_id_by_websocket[websocket].add(request_id)

    async def unbind_all(self, websocket: WebSocket, /) -> None:
        """Unbind everything from a websocket.

        :param websocket: The websocket to unbind.
        """
        for by_websocket, by_key in (
            (
                self.callback_state_by_websocket,
                self.websocket_by_callback_state,
            ),
            (
                self.powens_domain_by_websocket,
                self.websocket_by_powens_domain,
            ),
            (
                self.openid_ciba_request_id_by_websocket,
                self.websocket_by_openid_ciba_request_id,
            ),
        ):
            keys: set[Any] = by_websocket.pop(websocket, set())
            for key in keys:
                websocket_set = by_key[key]

                try:
                    websocket_set.remove(websocket)
                except KeyError:  # pragma: no cover
                    pass
                else:
                    if not websocket_set:
                        try:
                            del by_key[key]
                        except KeyError:  # pragma: no cover
                            pass

    async def push(
        self,
        message: Any,
        /,
    ) -> None:
        """Push a message.

        :param message: The message to push.
        """
        if isinstance(message, CallbackMessage):
            state = message.state
            push_message = CallbackServerMessage(
                timestamp=message.timestamp,
                state=state,
                url=message.url,
            ).json(separators=(',', ':'))

            gather_asyncio(*(
                websocket.send_text(push_message)
                for websocket in self.websocket_by_callback_state[state]
            ))
        elif isinstance(message, OpenIDCIBACallbackMessage):
            request_id = message.request_id
            push_message = OpenIDCIBACallbackServerMessage(
                timestamp=message.timestamp,
                request_id=request_id,
                access_token=message.access_token,
                push_token=message.push_token,
                push_error=message.push_error,
            ).json(separators=(',', ':'))

            gather_asyncio(*(
                websocket.send_text(push_message)
                for websocket in (
                    self.websocket_by_openid_ciba_request_id[request_id]
                )
            ))
        elif isinstance(message, PowensWebhookMessage):
            domain = message.domain
            push_message = PowensWebhookServerMessage(
                timestamp=message.timestamp,
                domain=domain,
                event=message.event,
                hmac_signature=message.hmac_signature,
                user_token=message.user_token,
                payload=message.payload,
            ).json(separators=(',', ':'))

            gather_asyncio(*(
                websocket.send_text(push_message)
                for websocket in self.websocket_by_powens_domain[domain]
            ))
