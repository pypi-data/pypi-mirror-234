from typing import overload
import abc

import System
import System.Security
import System.Security.Permissions


class SecurityPermissionFlag(System.Enum):
    """Obsoletions.CodeAccessSecurityMessage"""

    AllFlags = 16383

    Assertion = 1

    BindingRedirects = 8192

    ControlAppDomain = 1024

    ControlDomainPolicy = 256

    ControlEvidence = 32

    ControlPolicy = 64

    ControlPrincipal = 512

    ControlThread = 16

    Execution = 8

    Infrastructure = 4096

    NoFlags = 0

    RemotingConfiguration = 2048

    SerializationFormatter = 128

    SkipVerification = 4

    UnmanagedCode = 2


class SecurityAction(System.Enum):
    """Obsoletions.CodeAccessSecurityMessage"""

    Assert = 3

    Demand = 2

    Deny = 4

    InheritanceDemand = 7

    LinkDemand = 6

    PermitOnly = 5

    RequestMinimum = 8

    RequestOptional = 9

    RequestRefuse = 10


class SecurityAttribute(System.Attribute, metaclass=abc.ABCMeta):
    """Obsoletions.CodeAccessSecurityMessage"""

    @property
    def Action(self) -> int:
        """This property contains the int value of a member of the System.Security.Permissions.SecurityAction enum."""
        ...

    @property
    def Unrestricted(self) -> bool:
        ...

    def __init__(self, action: System.Security.Permissions.SecurityAction) -> None:
        """This method is protected."""
        ...

    def CreatePermission(self) -> System.Security.IPermission:
        ...


class CodeAccessSecurityAttribute(System.Security.Permissions.SecurityAttribute, metaclass=abc.ABCMeta):
    """Obsoletions.CodeAccessSecurityMessage"""

    def __init__(self, action: System.Security.Permissions.SecurityAction) -> None:
        """This method is protected."""
        ...


class SecurityPermissionAttribute(System.Security.Permissions.CodeAccessSecurityAttribute):
    """Obsoletions.CodeAccessSecurityMessage"""

    @property
    def Assertion(self) -> bool:
        ...

    @property
    def BindingRedirects(self) -> bool:
        ...

    @property
    def ControlAppDomain(self) -> bool:
        ...

    @property
    def ControlDomainPolicy(self) -> bool:
        ...

    @property
    def ControlEvidence(self) -> bool:
        ...

    @property
    def ControlPolicy(self) -> bool:
        ...

    @property
    def ControlPrincipal(self) -> bool:
        ...

    @property
    def ControlThread(self) -> bool:
        ...

    @property
    def Execution(self) -> bool:
        ...

    @property
    def Flags(self) -> int:
        """This property contains the int value of a member of the System.Security.Permissions.SecurityPermissionFlag enum."""
        ...

    @property
    def Infrastructure(self) -> bool:
        ...

    @property
    def RemotingConfiguration(self) -> bool:
        ...

    @property
    def SerializationFormatter(self) -> bool:
        ...

    @property
    def SkipVerification(self) -> bool:
        ...

    @property
    def UnmanagedCode(self) -> bool:
        ...

    def __init__(self, action: System.Security.Permissions.SecurityAction) -> None:
        ...

    def CreatePermission(self) -> System.Security.IPermission:
        ...


class PermissionState(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    Unrestricted = 1


