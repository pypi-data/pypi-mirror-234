"""Environment package."""
__all__ = (
    "environment",
)

import sys

from nodeps import Env


def environment() -> None:
    """Parses all globals in :obj:`__all__` of the module imported from environment variables.

    Parses:
        - bool: 1, 0, True, False, yes, no, on, off (case insensitive)
        - int: integer only numeric characters but 1 and 0 or SUDO_UID or SUDO_GID
        - ipaddress: ipv4/ipv6 address
        - url: if "//" or "@" is found it will be parsed as url
        - path: start with / or ~ or .
        - others as string

    Examples:
        >>> from nodeps import Path
        >>> from envg.default import *
        >>> assert isinstance(USER, str)
        >>> assert isinstance(PWD, Path)

    Returns:
        None
    """
    data = sys._getframe(1).f_globals
    for variable in data["__all__"]:
        data[variable] = Env.parse_as_bool(variable)
