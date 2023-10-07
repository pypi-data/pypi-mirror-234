#
# Copyright (c) 2012-2022 Snowflake Computing Inc. All rights reserved.
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#

"""Context module for pystarburst."""
import pystarburst


def get_active_session() -> "pystarburst.Session":
    """Returns the current active pystarburst session.

    Raises: PyStarburstSessionException: If there is more than one active session or no active sessions.

    Returns:
        A :class:`Session` object for the current session.
    """
    return pystarburst.session._get_active_session()
