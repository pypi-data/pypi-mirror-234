from typing import overload
import abc

import System
import System.Security.Principal


class PrincipalPolicy(System.Enum):
    """This class has no documentation."""

    UnauthenticatedPrincipal = 0

    NoPrincipal = 1

    WindowsPrincipal = 2


class IIdentity(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IPrincipal(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class TokenImpersonationLevel(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    Anonymous = 1

    Identification = 2

    Impersonation = 3

    Delegation = 4


