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
"""Redis related utilities for TeaL."""

from __future__ import annotations

from datetime import datetime
from logging import getLogger

from pydantic import (
    BaseModel, BaseSettings, Field, RedisDsn, ValidationError, parse_obj_as,
)
from pydantic.networks import HttpUrl
from redis.asyncio import Redis

logger = getLogger(__name__)


class RedisSettings(BaseSettings):
    """RabbitMQ related settings."""

    redis_dsn: RedisDsn = Field(env='REDIS_URL')
    """Redis connection URI to use.

    An example Redis URI for localhost is the following::

        redis://localhost:6379/0
    """


class StoredState(BaseModel):
    """Storage model as found in Redis for callbacks."""

    expires_at: datetime | None = None
    """UTC date and time at which the stored state should expire."""

    final_redirect_url: HttpUrl | None = None
    """The complete redirect URL to redirect the end user to.

    This can be non-specified; in such cases, instead of redirecting the
    end user, we just return an HTTP 2xx response.
    """

    with_fragment: bool = False
    """Whether to read the fragment."""


async def get_stored_state(
    state: str, /, *,
    settings: RedisSettings,
) -> StoredState | None:
    """Get the stored state.

    :param state: The state identifier to look for.
    :param settings: The Redis settings to use to find the stored state.
    :return: The stored state, or None if the state wasn't found.'
    """
    client: Redis = Redis.from_url(
        str(settings.redis_dsn),
        decode_responses=True,
    )

    raw_obj = await client.get('callback_' + state)
    if raw_obj is None:
        logger.info('No callback data found for state "%s".', state)
        return None

    try:
        obj = StoredState.parse_raw(raw_obj)
    except ValueError:
        logger.warning(
            'Could not parse found callback data for state "%s".',
            state,
            exc_info=True,
        )
        return None

    if obj.expires_at is not None and datetime.utcnow() >= obj.expires_at:
        logger.info(
            'Found callback data for state "%s" expired on %s, removing.',
            state,
            obj.expires_at.isoformat(),
        )
        await client.delete('callback_' + state)
        return None

    if obj.expires_at is not None:
        logger.info(
            'Callback data was found for state "%s", will expire on %s.',
            state,
            obj.expires_at.isoformat(),
        )
    else:
        logger.warning(
            'Callback data was found for state "%s", with no expiration date!',
            state,
        )

    return obj


async def store_state(
    state: str, /, *,
    final_redirect_url: str | None,
    with_fragment: bool = False,
    expires_at: datetime | None = None,
    settings: RedisSettings,
) -> None:
    """Store a callback state.

    :param state: The state to register.
    :param final_redirect_url: The complete redirect URL to redirect the
        end user to.
    :param with_fragment: Whether to read the fragment or not.
    """
    try:
        final_redirect_url = parse_obj_as(HttpUrl | None, final_redirect_url)
    except ValidationError as exc:
        raise ValueError(
            f'Invalid redirect URL: {exc.errors()[0]["msg"]}',
        ) from exc

    client: Redis = Redis.from_url(
        str(settings.redis_dsn),
        decode_responses=True,
    )

    await client.set(
        'callback_' + state,
        StoredState(
            final_redirect_url=final_redirect_url,
            with_fragment=with_fragment,
            expires_at=expires_at,
        ).json(separators=(',', ':')),
    )
