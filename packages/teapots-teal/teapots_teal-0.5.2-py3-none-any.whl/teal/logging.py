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
"""General utilities for all TeaL applications."""

from __future__ import annotations

import re
from collections.abc import Callable
from contextvars import ContextVar, Token as ContextToken
from logging import LogRecord, getLogRecordFactory, setLogRecordFactory
from time import gmtime
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Response
from pydantic import BaseModel
from pythonjsonlogger.jsonlogger import RESERVED_ATTRS, JsonFormatter
from starlette.middleware.base import (
    BaseHTTPMiddleware, RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.types import ASGIApp

SENSITIVE_CREDENTIALS_QUERY_PARAM_RE = re.compile(
    r'credentials=[A-Za-z0-9+/]+=*',
)


class RequestLoggingContext(BaseModel):
    """Logging properties."""

    request_id: str | None
    """Identifier for the current request."""


_logging_context_var: ContextVar[RequestLoggingContext | None] = ContextVar(
    '_logging_context_var',
    default=None,
)
"""Logging context variable.

This is set when dispatching a request from an initialized middleware.
"""


def get_current_context() -> RequestLoggingContext | None:
    """Get the current logging context.

    :return: A reference to the current logging context.
    """
    return _logging_context_var.get()


def make_log_record(
    *,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    original_factory: Callable[..., LogRecord],
) -> LogRecord:
    """Make a log record with contextual information.

    :param args: The positional arguments to the factory.
    :param kwargs: The keyword arguments to the factory.
    :param original_factory: The original factory to call first.
    :return: The log record to pass to the handlers.
    """
    record = original_factory(*args, **kwargs)

    # Evaluate the record message if there still are args.
    record.msg = record.getMessage()
    record.args = ()

    # Anonymize the credentials in the message if necessary.
    record.msg = SENSITIVE_CREDENTIALS_QUERY_PARAM_RE.sub(
        'credentials=XXX',
        record.msg,
    )

    # Add information based on the current context.
    ctx = get_current_context()
    if ctx is None:
        return record

    if ctx.request_id is not None:
        record.__dict__['request_id'] = ctx.request_id

    return record


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for setting logging utilities per request."""

    def __init__(self, app: ASGIApp):
        """Construct the logging middleware."""
        super().__init__(app)

        # We want to set the log factory to set request information on every
        # log produced in the context of the request, even with loggers
        # produced using ``logging.getLogger`` prior to the instantiation of
        # the logging middleware.
        original_factory = getLogRecordFactory()
        setLogRecordFactory(
            lambda *args, **kwargs: make_log_record(
                args=args,
                kwargs=kwargs,
                original_factory=original_factory,
            ),
        )

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Dispatch the request.

        :param request: The request to dispatch.
        :param call_next: The ASGI app to call next.
        :return: The next request.
        """
        request_id = request.headers.get('X-Request-ID')
        if not request_id:  # None or empty header.
            request_id = str(uuid4())

        request.state.request_id = request_id

        ctx = RequestLoggingContext(request_id=request_id)
        token: ContextToken = _logging_context_var.set(ctx)
        try:
            response = await call_next(request)
            response.headers['X-Request-ID'] = request_id
            return response
        finally:
            _logging_context_var.reset(token)


class LoggingFastAPI(FastAPI):
    """FastAPI application with the logging middleware at top level."""

    def build_middleware_stack(self) -> ASGIApp:
        """Build the middleware stack.

        This is overridden to have the logging middleware at top of the
        middleware stack, to also handle exceptions automatically.

        :return: The wrapped ASGI app.
        """
        app = super().build_middleware_stack()
        return LoggingMiddleware(app=app)


class RequestFormatter(JsonFormatter):
    """Formatter for all logs from TeaL."""

    # We want to always UTC instead of local time.
    converter = gmtime

    def __init__(self, *args, **kwargs):
        super().__init__(
            rename_fields={'asctime': 'time', 'levelname': 'level'},
            fmt=(
                '%(asctime)s %(levelname)s %(module)s %(name)s %(funcName)s '
                + '%(lineno)d %(message)s'
            ),
            reserved_attrs=tuple(
                set(RESERVED_ATTRS).difference({
                    'asctime',
                    'levelname',
                }),
            ),
            datefmt='%Y-%m-%dT%H:%M:%S',
        )
