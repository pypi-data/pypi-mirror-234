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
"""Configuration for the TeaL websocket dispatcher."""

from __future__ import annotations

from pydantic import AnyHttpUrl, Field, StrictStr, validator

from teal.amq import AMQSettings
from teal.redis import RedisSettings

__all__ = ['Settings']


class Settings(AMQSettings, RedisSettings):
    """Settings for the TeaL dispatcher."""

    listener_url: AnyHttpUrl = Field(env='LISTENER_URL')
    """Base URL for the listener, for communicating metadata to clients.

    Example definitions for this field::

        http://localhost:8080/
        https://events.teapots.fr/
        https://example.org/teal-listener/

    Note that the trailing slash is required for this setting to be used
    properly; otherwise, the last component of the path will likely be
    ignored.
    """

    password: StrictStr = Field(min_length=1, env='PASSWORD')
    """The password to authenticate with the websocket dispatcher."""

    @validator('listener_url')
    def normalize_listener_url(
        cls,
        value: AnyHttpUrl,
        **kwargs,
    ) -> AnyHttpUrl:
        """Ensure that the listener URL, once configured, has a trailing slash.

        :param value: The value to normalize.
        :return: The normalized value.
        """
        path = value.path or ''
        if not path.endswith('/'):
            path += '/'

        # Change path, and remove query string and fragment.
        new_kwargs = dict(
            scheme=value.scheme,
            user=value.user,
            password=value.password,
            host=value.host,
            port=value.port,
            path=path,
        )
        return AnyHttpUrl(AnyHttpUrl.build(**new_kwargs), **new_kwargs)
