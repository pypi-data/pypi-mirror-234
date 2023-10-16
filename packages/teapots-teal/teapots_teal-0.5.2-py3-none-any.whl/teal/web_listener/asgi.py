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
"""ASGI application for the TeaL web listener."""

from __future__ import annotations

import os
import re
from datetime import datetime, timedelta
from functools import lru_cache
from logging import getLogger

from fastapi import BackgroundTasks, Depends, Path, Query, Request
from fastapi.responses import PlainTextResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import parse_obj_as
from starlette.status import HTTP_204_NO_CONTENT, HTTP_302_FOUND

from teal.amq import (
    AMQHandler, CallbackMessage, Message, OpenIDCIBACallbackMessage,
    OpenIDCIBAPushError, OpenIDCIBAPushToken, PowensWebhookMessage,
)
from teal.logging import LoggingFastAPI

from .config import Settings
from .exceptions import (
    InvalidCIBAAuthentication, InvalidCIBAPayload, MissingFullURLException,
    MissingStateException, NoRedirectionException,
    PowensWebhookClientException, WebListenerException,
)
from .utils import (
    CallbackStateInformation, OpenIDCIBAPingPayload,
    OpenIDCIBAPushErrorPayload, OpenIDCIBAPushTokenPayload,
    QueryStringMiddleware, fix_url_query_separator, get_powens_hmac_signature,
    get_powens_user_token,
)

__all__ = ['app']

logger = getLogger(__name__)

NOTIFICATION_TOKEN_RE = re.compile(r'[a-z0-9.~+/_=-]{1,1024}')

app = LoggingFastAPI(docs_url=None, redoc_url=None, openapi_url=None)
"""ASGI application definition for the listener."""

app.add_middleware(QueryStringMiddleware, delimiter='&')

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), 'templates'),
)
static_files = StaticFiles(
    directory=os.path.join(os.path.dirname(__file__), 'static'),
)


async def send_message(
    message: Message,
    /,
    *,
    settings: Settings,
) -> None:  # pragma: no cover
    """Send a message on an AMQ queue.

    :param message: Message to send.
    """
    # NOTE: This is not covered since it is considered tested in
    # ``tests/test_amq.py``.
    async with AMQHandler.handler_context(settings=settings) as handler:
        await handler.send(message)


@lru_cache()
def get_settings() -> Settings:
    """Get settings instanciated per request."""
    return Settings()


@app.get('/favicon.png')
@app.get('/favicon.ico')
@app.get('/robots.txt')
async def get_static_file(request: Request) -> Response:
    """Get static files."""
    _, _, filename = request.url.path.rpartition('/')
    return await static_files.get_response(filename, request.scope)


@app.exception_handler(WebListenerException)
async def handle_business_exception(
    request: Request,
    exc: WebListenerException,
) -> Response:
    """Handle exceptions to return them as a plaintext response.

    This makes it easier to test, and when evaluated by servers, to parse.
    For example, Powens allow returning the direct responses from the
    webhook receiver by mail and through logs, so the simpler the better.
    """
    if exc.status_code == HTTP_204_NO_CONTENT:
        return Response(status_code=exc.status_code, background=exc.background)

    return PlainTextResponse(
        content=exc.detail + '\n',
        status_code=exc.status_code,
        background=exc.background,
    )


# ---
# Callback management.
# ---


@app.get('/callback')
@app.get('/errback')
async def get_callback(
    request: Request,
    background_tasks: BackgroundTasks,
    settings: Settings = Depends(get_settings),
) -> Response:
    """Get a callback event from an end user."""
    try:
        info = await CallbackStateInformation.from_url(
            str(request.url),
            request=request,
            settings=settings,
        )
    except MissingStateException:
        # We suppose that the state is located in the fragment, so we need
        # to redirect to the raw callback endpoint with the full URL including
        # the fragment.
        logger.info(
            'Missing state, we want to redirect to the raw callback endpoint '
            + 'to get one from the fragment if available.',
        )
        return templates.TemplateResponse(
            'fragment.html',
            {'request': request},
        )

    if info.with_fragment:
        # We need to get the fragment, even though we have the state.
        return templates.TemplateResponse(
            'fragment.html',
            {'request': request},
        )

    background_tasks.add_task(
        send_message,
        CallbackMessage(
            url=str(request.url),
            state=info.state,
        ),
        settings=settings,
    )

    if info.final_redirect_url is None:
        logger.info('Stopping redirection here.')
        raise NoRedirectionException(background=background_tasks)

    logger.info('Redirecting the end user to: %s', info.final_redirect_url)
    return RedirectResponse(
        info.final_redirect_url,
        status_code=HTTP_302_FOUND,
    )


@app.get('/raw-callback')
async def get_raw_callback(
    request: Request,
    background_tasks: BackgroundTasks,
    full_url: str | None = Query(
        default=None,
        example='https://events.teapots.fr/callback#state=123',
    ),  # noqa: B008
    settings: Settings = Depends(get_settings),
) -> Response:
    """Get a raw callback event from an end user."""
    if full_url is None:
        # We suppose that the state is located in the fragment, so we need
        # to redirect to the raw callback endpoint with the full URL including
        # the fragment.
        raise MissingFullURLException()

    full_url = fix_url_query_separator(full_url)
    info = await CallbackStateInformation.from_url(
        full_url,
        request=request,
        settings=settings,
    )

    background_tasks.add_task(
        send_message,
        CallbackMessage(
            url=full_url,
            state=info.state,
        ),
        settings=settings,
    )

    if info.final_redirect_url is None:
        logger.info('Stopping redirection here.')
        raise NoRedirectionException(background=background_tasks)

    logger.info('Redirecting the end user to: %s', info.final_redirect_url)
    return RedirectResponse(
        info.final_redirect_url,
        status_code=HTTP_302_FOUND,
    )


# ---
# OpenID CIBA management.
# ---


@app.post('/openid-ciba-callback')
async def post_openid_ciba_callback(
    request: Request,
    background_tasks: BackgroundTasks,
    settings: Settings = Depends(get_settings),
) -> Response:
    """Get an OpenID Connect CIBA Ping or Push callback."""
    authorization = request.headers.get('Authorization')
    if authorization is None:
        logger.info('Missing Authorization header.')
        raise InvalidCIBAAuthentication()

    token_type, separator, access_token = authorization.partition(' ')
    if (
        token_type.casefold() != 'bearer'
        or separator != ' '
        or not NOTIFICATION_TOKEN_RE.fullmatch(access_token)
    ):
        logger.info('Invalid format for the Authorization header.')
        raise InvalidCIBAAuthentication()

    try:
        payload = parse_obj_as(
            OpenIDCIBAPingPayload
            | OpenIDCIBAPushTokenPayload
            | OpenIDCIBAPushErrorPayload,
            await request.json(),
        )
    except ValueError as exc:
        logger.warning(
            'Could not parse the payload as an OpenID CIBA payload:',
            exc_info=True,
        )

        try:
            logger.info(
                'Payload body was the following:\n%s',
                (await request.body()).decode('utf-8'),
            )
        except ValueError:
            pass  # Bad encoding, this will have been described in the warning.

        raise InvalidCIBAPayload() from exc

    if isinstance(payload, OpenIDCIBAPingPayload):
        logger.info(
            'Request was an OpenID CIBA Ping for request %s',
            payload.auth_req_id,
        )
        message = OpenIDCIBACallbackMessage(
            request_id=payload.auth_req_id,
            access_token=access_token,
        )
    elif isinstance(payload, OpenIDCIBAPushTokenPayload):
        logger.info(
            'Request was an OpenID CIBA Push Token for request %s',
            payload.auth_req_id,
        )
        message = OpenIDCIBACallbackMessage(
            request_id=payload.auth_req_id,
            access_token=access_token,
            push_token=OpenIDCIBAPushToken(
                access_token=payload.access_token,
                token_type=payload.token_type,
                refresh_token=payload.refresh_token,
                expires_at=(
                    datetime.utcnow() + timedelta(seconds=payload.expires_in)
                ),
                id_token=payload.id_token,
            ),
        )
    elif isinstance(payload, OpenIDCIBAPushErrorPayload):
        logger.info(
            'Request was an OpenID CIBA Push Error for request %s',
            payload.auth_req_id,
        )
        message = OpenIDCIBACallbackMessage(
            request_id=payload.auth_req_id,
            access_token=access_token,
            push_error=OpenIDCIBAPushError(
                error=payload.error,
                error_description=payload.error_description,
            ),
        )

    background_tasks.add_task(send_message, message, settings=settings)
    return Response(
        b'',
        status_code=HTTP_204_NO_CONTENT,
        background=background_tasks,
    )


# ---
# Powens webhooks management.
# ---


@app.post('/powens-webhook/{domain}/{event}')
async def get_powens_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    domain: str = Path(
        example='budgea.biapi.pro',
    ),  # noqa: B008
    event: str = Path(
        example='USER_CREATED',
    ),  # noqa: B008
    settings: Settings = Depends(get_settings),
) -> Response:
    """Get a Powens webhook push."""
    if not domain.endswith('.biapi.pro') or len(domain) <= 10:
        raise PowensWebhookClientException(detail=(
            'Webhook misconfiguration: endpoint must contain the ".biapi.pro" '
            + 'suffix, such as: '
            + str(request.url_for(
                'get_powens_webhook',
                domain=domain + '.biapi.pro',
                event=event,
            ))
        ))

    hmac_signature = get_powens_hmac_signature(request)
    user_token = get_powens_user_token(request)

    if hmac_signature is None and user_token is None:
        raise PowensWebhookClientException(detail=(
            'Webhook misconfiguration: user-scoped token or HMAC '
            + 'authentication required.'
        ))

    payload: bytes = await request.body()

    background_tasks.add_task(
        send_message,
        PowensWebhookMessage(
            domain=domain,
            event=event,
            hmac_signature=hmac_signature,
            user_token=user_token,
            payload=payload.decode('UTF-8'),
        ),
        settings=settings,
    )

    return Response(
        b'',
        status_code=HTTP_204_NO_CONTENT,
        background=background_tasks,
    )
