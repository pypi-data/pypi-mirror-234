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
"""ASGI application for the TeaL websocket dispatcher."""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from logging import getLogger
from typing import AsyncIterator
from urllib.parse import urljoin

from fastapi import (
    Depends, Request, WebSocket, WebSocketDisconnect, WebSocketException,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.status import WS_1008_POLICY_VIOLATION

from teal import __version__ as teal_version
from teal.logging import LoggingFastAPI
from teal.redis import store_state

from .config import Settings
from .protocol import (
    CallbackCreation, CallbackCreationFailedServerMessage,
    CallbackRegistration, ClientMessage, OpenIDCIBACallbackRegistration,
    PowensDomainRegistration,
)
from .utils import BasicAuthBackend, WebsocketDispatcher

__all__ = ['app']

logger = getLogger(__name__)

dispatcher: WebsocketDispatcher


@lru_cache()
def get_settings() -> Settings:
    """Get settings instanciated per request."""
    return Settings()


@asynccontextmanager
async def lifespan(app: LoggingFastAPI) -> AsyncIterator[None]:
    global dispatcher

    settings = get_settings()
    async with WebsocketDispatcher.dispatcher_context(
        settings=settings,
    ) as dispatcher:
        yield


app = LoggingFastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)
"""ASGI application definition for the dispatcher."""

app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/.well-known/teapots-teal-metadata')
async def get_metadata(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> Response:
    """Get TeaL dispatcher metadata.

    Note that this endpoint does not require authentication.
    """
    return JSONResponse({
        'server_version': teal_version,
        'websocket_url': str(request.url_for('get_websocket')),
        'callback_url': urljoin(settings.listener_url, 'callback'),
        'errback_url': urljoin(settings.listener_url, 'errback'),
        'openid_ciba_callback_url': urljoin(
            settings.listener_url,
            'openid-ciba-callback',
        ),
    })


@app.websocket('/websocket')
async def get_websocket(
    websocket: WebSocket,
    settings: Settings = Depends(get_settings),
) -> None:
    """Get the websocket, for communication."""
    if websocket.auth is None:
        raise WebSocketException(
            code=WS_1008_POLICY_VIOLATION,
            reason='Authentication required',
        )

    try:
        await websocket.accept()

        while True:
            data = await websocket.receive_text()
            try:
                message = ClientMessage.parse_raw(data)
            except ValueError:
                continue

            creation = message.create
            if creation is None:
                pass
            elif isinstance(creation, CallbackCreation):
                expires_at = creation.expires_at
                if expires_at.tzinfo:
                    expires_at = expires_at.astimezone(timezone.utc).replace(
                        tzinfo=None,
                    )

                callback_failure: (
                    CallbackCreationFailedServerMessage | None
                ) = None
                utcnow = datetime.utcnow() + timedelta(seconds=10)
                if expires_at < utcnow:
                    # Creation date and time are too early.
                    callback_failure = CallbackCreationFailedServerMessage(
                        state=creation.state,
                        detail='Callback expiration date was too early.',
                    )
                elif expires_at > utcnow + timedelta(days=7):
                    # Creation date and time are too late.
                    callback_failure = CallbackCreationFailedServerMessage(
                        state=creation.state,
                        detail='Callback expiration was too late; a maximum '
                        + 'of 7 days is enforced.',
                    )

                if callback_failure is not None:
                    await websocket.send_text(
                        callback_failure.json(separators=(',', ':')),
                    )
                    continue

                await store_state(
                    creation.state,
                    final_redirect_url=creation.final_redirect_url,
                    with_fragment=creation.with_fragment,
                    expires_at=expires_at,
                    settings=settings,
                )

            registration = message.register_to
            if registration is None:
                pass
            elif isinstance(registration, CallbackRegistration):
                await dispatcher.bind_callback_state(
                    websocket,
                    state=registration.state,
                )
            elif isinstance(registration, OpenIDCIBACallbackRegistration):
                await dispatcher.bind_openid_ciba_request_identifier(
                    websocket,
                    request_id=registration.request_id,
                )
            elif isinstance(registration, PowensDomainRegistration):
                await dispatcher.bind_powens_domain(
                    websocket,
                    domain=registration.powens_domain,
                )

            # NOTE: We ignore other registrations.
    except WebSocketDisconnect:
        # We don't care about this.
        pass
    finally:
        await dispatcher.unbind_all(websocket)
