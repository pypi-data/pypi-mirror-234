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
"""Configuration for the TeaL web listener."""

from __future__ import annotations

from pydantic import Field

from teal.amq import AMQSettings
from teal.redis import RedisSettings

__all__ = ['Settings']


class Settings(AMQSettings, RedisSettings):
    """Settings for the TeaL listener."""

    powens_redirect_fallback: bool = Field(
        default=False,
        env='POWENS_REDIRECT_FALLBACK',
    )
    """In case of an unknown state, whether to use Powens-style fallback.

    This is mostly useful if the TeaL Web Listener is to be used as a
    callback bouncer for a white label customer. It implements callback
    state formats used with Powens' bouncer.
    """
