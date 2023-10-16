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
"""Definitions for the TeaL Websocket Dispatcher protocol."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field
from pydantic.networks import HttpUrl

from teal.amq import (
    OpenIDCIBAPushError, OpenIDCIBAPushToken, PowensHMACSignature,
)

# ---
# Client messages.
# ---


class CallbackCreation(BaseModel):
    """Data to create a stored callback data."""

    type: Literal['callback']
    """Callback creation type, as a discriminant."""

    state: str
    """The state to create."""

    final_redirect_url: HttpUrl | None = None
    """Final redirect URL."""

    with_fragment: bool = False
    """Whether to get the fragment with the redirect or not."""

    expires_at: datetime
    """Expiration date for the callback creation."""


class CallbackRegistration(BaseModel):
    """Registration for callback states."""

    type: Literal['callback']
    """Callback register type, as a discriminant."""

    state: str
    """The state to register to."""


class OpenIDCIBACallbackRegistration(BaseModel):
    """Registration for OpenID CIBA callbacks for a given request."""

    type: Literal['openid_ciba_callback']
    """OpenID CIBA callback registration type, as a discriminant."""

    request_id: str
    """The request identifier to register to."""


class PowensDomainRegistration(BaseModel):
    """Registration for events related to a Powens domain."""

    type: Literal['powens_domain']
    """Powens domain register type."""

    powens_domain: str
    """The Powens domain to register, without the '.biapi.pro' domain part."""


class ClientMessage(BaseModel):
    """Message for registering to one or more set of events."""

    create: CallbackCreation | None = Field(default=None)
    """Element to create in the database."""

    register_to: (
        CallbackRegistration
        | OpenIDCIBACallbackRegistration
        | PowensDomainRegistration
        | None
    ) = Field(
        default=None,
        discriminator='type',
    )
    """Event to register to."""


# ---
# Server messages.
# ---


class CallbackCreationFailedServerMessage(BaseModel):
    """Message signalling that registering a callback has failed."""

    type: Literal['callback_creation_failure'] = ('callback_creation_failure')
    """Message type, for allowing discrimination at caller level."""

    state: str
    """State for which the callback event binding has failed."""

    detail: str
    """Human-readable creation failure detail."""


class CallbackServerMessage(BaseModel):
    """Message produced by the server when a callback event occurs."""

    type: Literal['callback'] = ('callback')
    """Message type, for allowing discrimination at caller level."""

    timestamp: datetime
    """Timestamp at which the message was emitted."""

    url: str
    """Resulting callback URL with parameters and fragment."""

    state: str
    """State for which the callback is emitted."""


class OpenIDCIBACallbackServerMessage(BaseModel):
    """Message produced by the server when an OpenID callback event occurs."""

    type: Literal['openid_ciba_callback'] = ('openid_ciba_callback')
    """Message type, for allowing discrimination at caller level."""

    timestamp: datetime
    """Timestamp at which the message was emitted."""

    request_id: str
    """Authentication request identifier."""

    access_token: str
    """The access token used to authenticate the ping/push callback."""

    push_token: OpenIDCIBAPushToken | None = None
    """The token data, in case the callback is a push token."""

    push_error: OpenIDCIBAPushError | None = None
    """The error data, in case the callback is a push error."""


class PowensWebhookServerMessage(BaseModel):
    """Message produced by the server when a Powens webhook is called."""

    type: Literal['powens_webhook'] = ('powens_webhook')
    """Message type, for allowing discrimination at caller level."""

    timestamp: datetime
    """Timestamp at which the message was emitted."""

    domain: str
    """Domain for which the webhook is emitted."""

    event: str
    """Event for which the webhook is emitted."""

    hmac_signature: PowensHMACSignature | None
    """The HMAC signature, if present."""

    user_token: str | None
    """User scoped token with which the webhook is authenticated."""

    payload: str
    """The UTF-8 decoded payload."""
