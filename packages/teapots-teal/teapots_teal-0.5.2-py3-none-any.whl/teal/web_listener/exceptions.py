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
"""Exception definitions for the TeaL web listener."""

from __future__ import annotations

from starlette.background import BackgroundTasks
from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST


class WebListenerException(Exception):
    """Exception raised by routes and utilities from the Web Listener.

    :param status_code: The status code to raise.
    :param detail: The detail.
    :param background: The background task to include with the response.
    """

    __slots__ = ('background', 'detail', 'status_code')

    background: BackgroundTasks | None
    status_code: int
    detail: str

    def __init__(
        self,
        /,
        *,
        status_code: int | None = None,
        detail: str = '',
        background: BackgroundTasks | None = None,
    ) -> None:
        if status_code is None:
            status_code = HTTP_400_BAD_REQUEST

        self.background = background
        self.detail = detail
        self.status_code = status_code


# ---
# Callback-related exceptions.
# ---


class WebListenerCallbackException(WebListenerException):
    """Callback-related exceptions raised by the Web Listener."""

    def __init__(
        self,
        detail: str,
        /,
        *,
        status_code: int | None = None,
        background: BackgroundTasks | None = None,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail,
            background=background,
        )


class MissingStateException(WebListenerCallbackException):
    """The state could not be found in a given URL."""

    def __init__(self, /):
        super().__init__('Missing state in full URL')


class EmptyStateException(WebListenerCallbackException):
    """A callback state was found, but was empty."""

    def __init__(self, /):
        super().__init__('Empty state')


class UnknownStateException(WebListenerCallbackException):
    """A callback state was found, but not in the database."""

    def __init__(self, /):
        super().__init__('Unknown state')


class MissingFullURLException(WebListenerCallbackException):
    """The full URL was not provided."""

    def __init__(self, /):
        super().__init__('Missing full URL')


class NoRedirectionException(WebListenerCallbackException):
    """No redirection is implied by the callback state."""

    def __init__(self, /, *, background: BackgroundTasks | None = None):
        super().__init__(
            'No redirection at the end of process',
            status_code=HTTP_204_NO_CONTENT,
            background=background,
        )


# ---
# OpenID CIBA related exceptions.
# ---


class WebListenerCIBAException(WebListenerException):
    """OpenID CIBA Ping/Push related exceptions raised by the Web Listener."""

    def __init__(
        self,
        detail: str,
        /,
        *,
        status_code: int | None = None,
        background: BackgroundTasks | None = None,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail,
            background=background,
        )


class InvalidCIBAAuthentication(WebListenerCIBAException):
    """An invalid authentication was provided with the ping/push callback."""

    def __init__(self, /):
        super().__init__('Invalid authentication')


class InvalidCIBAPayload(WebListenerCIBAException):
    """An invalid payload was provided with the ping/push callback."""

    def __init__(self, /):
        super().__init__('Invalid payload')


# ---
# Powens webhook related exceptions.
# ---


class PowensWebhookClientException(WebListenerException):
    """A Powens webhook validation has failed.

    :param status_code: The status code to use to signal the error.
        If None, the exception will be reported using the HTTP 400 status
        code.
    """

    def __init__(self, /, *, status_code: int | None = None, detail: str):
        super().__init__(status_code=status_code, detail=detail)
