from typing import overload
import abc
import typing
import warnings

import System
import System.Collections
import System.Reflection
import System.Runtime.Serialization
import System.Security
import System.Security.Permissions


class SecurityCriticalScope(System.Enum):
    """SecurityCriticalScope is only used for .NET 2.0 transparency compatibility."""

    Explicit = 0

    Everything = ...


class SecurityCriticalAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Scope(self) -> int:
        """
        This property contains the int value of a member of the System.Security.SecurityCriticalScope enum.
        
        SecurityCriticalScope is only used for .NET 2.0 transparency compatibility.
        """
        warnings.warn("SecurityCriticalScope is only used for .NET 2.0 transparency compatibility.", DeprecationWarning)

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, scope: System.Security.SecurityCriticalScope) -> None:
        ...


class AllowPartiallyTrustedCallersAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def PartialTrustVisibilityLevel(self) -> int:
        """This property contains the int value of a member of the System.Security.PartialTrustVisibilityLevel enum."""
        ...

    def __init__(self) -> None:
        ...


class ISecurityEncodable(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IStackWalk(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IPermission(System.Security.ISecurityEncodable, metaclass=abc.ABCMeta):
    """Obsoletions.CodeAccessSecurityMessage"""


class SecurityElement(System.Object):
    """This class has no documentation."""

    @property
    def Tag(self) -> str:
        ...

    @property
    def Attributes(self) -> System.Collections.Hashtable:
        ...

    @property
    def Text(self) -> str:
        ...

    @property
    def Children(self) -> System.Collections.ArrayList:
        ...

    @overload
    def __init__(self, tag: str) -> None:
        ...

    @overload
    def __init__(self, tag: str, text: str) -> None:
        ...

    def AddAttribute(self, name: str, value: str) -> None:
        ...

    def AddChild(self, child: System.Security.SecurityElement) -> None:
        ...

    def Attribute(self, name: str) -> str:
        ...

    def Copy(self) -> System.Security.SecurityElement:
        ...

    def Equal(self, other: System.Security.SecurityElement) -> bool:
        ...

    @staticmethod
    def Escape(str: str) -> str:
        ...

    @staticmethod
    def FromString(xml: str) -> System.Security.SecurityElement:
        ...

    @staticmethod
    def IsValidAttributeName(name: str) -> bool:
        ...

    @staticmethod
    def IsValidAttributeValue(value: str) -> bool:
        ...

    @staticmethod
    def IsValidTag(tag: str) -> bool:
        ...

    @staticmethod
    def IsValidText(text: str) -> bool:
        ...

    def SearchForChildByTag(self, tag: str) -> System.Security.SecurityElement:
        ...

    def SearchForTextOfTag(self, tag: str) -> str:
        ...

    def ToString(self) -> str:
        ...


class PermissionSet(System.Object, System.Collections.ICollection, System.Runtime.Serialization.IDeserializationCallback, System.Security.ISecurityEncodable, System.Security.IStackWalk):
    """This class has no documentation."""

    @property
    def Count(self) -> int:
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def IsSynchronized(self) -> bool:
        ...

    @property
    def SyncRoot(self) -> System.Object:
        ...

    @overload
    def __init__(self, state: System.Security.Permissions.PermissionState) -> None:
        ...

    @overload
    def __init__(self, permSet: System.Security.PermissionSet) -> None:
        ...

    def AddPermission(self, perm: System.Security.IPermission) -> System.Security.IPermission:
        ...

    def AddPermissionImpl(self, perm: System.Security.IPermission) -> System.Security.IPermission:
        """This method is protected."""
        ...

    def Assert(self) -> None:
        ...

    def ContainsNonCodeAccessPermissions(self) -> bool:
        ...

    @staticmethod
    def ConvertPermissionSet(inFormat: str, inData: typing.List[int], outFormat: str) -> typing.List[int]:
        """This member is marked as obsolete."""
        warnings.warn("This member is marked as obsolete.", DeprecationWarning)

    def Copy(self) -> System.Security.PermissionSet:
        ...

    def CopyTo(self, array: System.Array, index: int) -> None:
        ...

    def Demand(self) -> None:
        ...

    def Deny(self) -> None:
        """This member is marked as obsolete."""
        warnings.warn("This member is marked as obsolete.", DeprecationWarning)

    def Equals(self, o: typing.Any) -> bool:
        ...

    def FromXml(self, et: System.Security.SecurityElement) -> None:
        ...

    def GetEnumerator(self) -> System.Collections.IEnumerator:
        ...

    def GetEnumeratorImpl(self) -> System.Collections.IEnumerator:
        """This method is protected."""
        ...

    def GetHashCode(self) -> int:
        ...

    def GetPermission(self, permClass: typing.Type) -> System.Security.IPermission:
        ...

    def GetPermissionImpl(self, permClass: typing.Type) -> System.Security.IPermission:
        """This method is protected."""
        ...

    def Intersect(self, other: System.Security.PermissionSet) -> System.Security.PermissionSet:
        ...

    def IsEmpty(self) -> bool:
        ...

    def IsSubsetOf(self, target: System.Security.PermissionSet) -> bool:
        ...

    def IsUnrestricted(self) -> bool:
        ...

    def PermitOnly(self) -> None:
        ...

    def RemovePermission(self, permClass: typing.Type) -> System.Security.IPermission:
        ...

    def RemovePermissionImpl(self, permClass: typing.Type) -> System.Security.IPermission:
        """This method is protected."""
        ...

    @staticmethod
    def RevertAssert() -> None:
        ...

    def SetPermission(self, perm: System.Security.IPermission) -> System.Security.IPermission:
        ...

    def SetPermissionImpl(self, perm: System.Security.IPermission) -> System.Security.IPermission:
        """This method is protected."""
        ...

    def ToString(self) -> str:
        ...

    def ToXml(self) -> System.Security.SecurityElement:
        ...

    def Union(self, other: System.Security.PermissionSet) -> System.Security.PermissionSet:
        ...


class PartialTrustVisibilityLevel(System.Enum):
    """This class has no documentation."""

    VisibleToAllHosts = 0

    NotVisibleByDefault = 1


class SecureString(System.Object, System.IDisposable):
    """This class has no documentation."""

    @property
    def Length(self) -> int:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, value: typing.Any, length: int) -> None:
        ...

    def AppendChar(self, c: str) -> None:
        ...

    def Clear(self) -> None:
        ...

    def Copy(self) -> System.Security.SecureString:
        ...

    def Dispose(self) -> None:
        ...

    def InsertAt(self, index: int, c: str) -> None:
        ...

    def IsReadOnly(self) -> bool:
        ...

    def MakeReadOnly(self) -> None:
        ...

    def RemoveAt(self, index: int) -> None:
        ...

    def SetAt(self, index: int, c: str) -> None:
        ...


class UnverifiableCodeAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class SecurityRuleSet(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    Level1 = 1

    Level2 = 2


class SecurityRulesAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def SkipVerificationInFullTrust(self) -> bool:
        ...

    @property
    def RuleSet(self) -> int:
        """This property contains the int value of a member of the System.Security.SecurityRuleSet enum."""
        ...

    def __init__(self, ruleSet: System.Security.SecurityRuleSet) -> None:
        ...


class SecuritySafeCriticalAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class VerificationException(System.SystemException):
    """This class has no documentation."""

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, innerException: System.Exception) -> None:
        ...

    @overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        This method is protected.
        
        Obsoletions.LegacyFormatterImplMessage
        """
        ...


class SecurityTreatAsSafeAttribute(System.Attribute):
    """SecurityTreatAsSafe is only used for .NET 2.0 transparency compatibility. Use the SecuritySafeCriticalAttribute instead."""

    def __init__(self) -> None:
        ...


class SecurityTransparentAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class SecurityException(System.SystemException):
    """This class has no documentation."""

    @property
    def Demanded(self) -> System.Object:
        ...

    @property
    def DenySetInstance(self) -> System.Object:
        ...

    @property
    def FailedAssemblyInfo(self) -> System.Reflection.AssemblyName:
        ...

    @property
    def GrantedSet(self) -> str:
        ...

    @property
    def Method(self) -> System.Reflection.MethodInfo:
        ...

    @property
    def PermissionState(self) -> str:
        ...

    @property
    def PermissionType(self) -> typing.Type:
        ...

    @property
    def PermitOnlySetInstance(self) -> System.Object:
        ...

    @property
    def RefusedSet(self) -> str:
        ...

    @property
    def Url(self) -> str:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...

    @overload
    def __init__(self, message: str, type: typing.Type) -> None:
        ...

    @overload
    def __init__(self, message: str, type: typing.Type, state: str) -> None:
        ...

    @overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        This method is protected.
        
        Obsoletions.LegacyFormatterImplMessage
        """
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """Obsoletions.LegacyFormatterImplMessage"""
        warnings.warn("Obsoletions.LegacyFormatterImplMessage", DeprecationWarning)

    def ToString(self) -> str:
        ...


class SuppressUnmanagedCodeSecurityAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


