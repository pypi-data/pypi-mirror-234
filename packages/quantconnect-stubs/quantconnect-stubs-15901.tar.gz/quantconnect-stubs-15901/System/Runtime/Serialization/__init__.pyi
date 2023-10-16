from typing import overload
import abc
import datetime
import typing
import warnings

import System
import System.Collections
import System.Runtime.Serialization


class ISerializable(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class DeserializationToken(System.IDisposable):
    """This class has no documentation."""

    def Dispose(self) -> None:
        ...


class ISafeSerializationData(metaclass=abc.ABCMeta):
    """Obsoletions.LegacyFormatterMessage"""


class OnDeserializedAttribute(System.Attribute):
    """This class has no documentation."""


class IFormatterConverter(metaclass=abc.ABCMeta):
    """Obsoletions.LegacyFormatterMessage"""


class SerializationEntry:
    """This class has no documentation."""

    @property
    def Value(self) -> System.Object:
        ...

    @property
    def Name(self) -> str:
        ...

    @property
    def ObjectType(self) -> typing.Type:
        ...


class SerializationInfoEnumerator(System.Object, System.Collections.IEnumerator):
    """This class has no documentation."""

    @property
    def Current(self) -> System.Runtime.Serialization.SerializationEntry:
        ...

    @property
    def Name(self) -> str:
        ...

    @property
    def Value(self) -> System.Object:
        ...

    @property
    def ObjectType(self) -> typing.Type:
        ...

    def MoveNext(self) -> bool:
        ...

    def Reset(self) -> None:
        ...


class SerializationInfo(System.Object):
    """The structure for holding all of the data needed for object serialization and deserialization."""

    @property
    def FullTypeName(self) -> str:
        ...

    @property
    def AssemblyName(self) -> str:
        ...

    @property
    def IsFullTypeNameSetExplicit(self) -> bool:
        ...

    @property
    def IsAssemblyNameSetExplicit(self) -> bool:
        ...

    @property
    def MemberCount(self) -> int:
        ...

    @property
    def ObjectType(self) -> typing.Type:
        ...

    @overload
    def __init__(self, type: typing.Type, converter: System.Runtime.Serialization.IFormatterConverter) -> None:
        """Obsoletions.LegacyFormatterMessage"""
        ...

    @overload
    def __init__(self, type: typing.Type, converter: System.Runtime.Serialization.IFormatterConverter, requireSameTokenInPartialTrust: bool) -> None:
        """Obsoletions.LegacyFormatterMessage"""
        ...

    @overload
    def AddValue(self, name: str, value: typing.Any, type: typing.Type) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: typing.Any) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: bool) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: str) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: int) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: float) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: float) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: float) -> None:
        ...

    @overload
    def AddValue(self, name: str, value: typing.Union[datetime.datetime, datetime.date]) -> None:
        ...

    def GetBoolean(self, name: str) -> bool:
        ...

    def GetByte(self, name: str) -> int:
        ...

    def GetChar(self, name: str) -> str:
        ...

    def GetDateTime(self, name: str) -> datetime.datetime:
        ...

    def GetDecimal(self, name: str) -> float:
        ...

    def GetDouble(self, name: str) -> float:
        ...

    def GetEnumerator(self) -> System.Runtime.Serialization.SerializationInfoEnumerator:
        ...

    def GetInt16(self, name: str) -> int:
        ...

    def GetInt32(self, name: str) -> int:
        ...

    def GetInt64(self, name: str) -> int:
        ...

    def GetSByte(self, name: str) -> int:
        ...

    def GetSingle(self, name: str) -> float:
        ...

    def GetString(self, name: str) -> str:
        ...

    def GetUInt16(self, name: str) -> int:
        ...

    def GetUInt32(self, name: str) -> int:
        ...

    def GetUInt64(self, name: str) -> int:
        ...

    def GetValue(self, name: str, type: typing.Type) -> System.Object:
        ...

    def SetType(self, type: typing.Type) -> None:
        ...

    @staticmethod
    def StartDeserialization() -> System.Runtime.Serialization.DeserializationToken:
        ...


class StreamingContextStates(System.Enum):
    """Obsoletions.LegacyFormatterMessage"""

    CrossProcess = ...

    CrossMachine = ...

    File = ...

    Persistence = ...

    Remoting = ...

    Other = ...

    Clone = ...

    CrossAppDomain = ...

    All = ...


class StreamingContext:
    """This class has no documentation."""

    @property
    def State(self) -> int:
        """
        This property contains the int value of a member of the System.Runtime.Serialization.StreamingContextStates enum.
        
        Obsoletions.LegacyFormatterMessage
        """
        warnings.warn("Obsoletions.LegacyFormatterMessage", DeprecationWarning)

    @property
    def Context(self) -> System.Object:
        ...

    @overload
    def __init__(self, state: System.Runtime.Serialization.StreamingContextStates) -> None:
        """Obsoletions.LegacyFormatterMessage"""
        ...

    @overload
    def __init__(self, state: System.Runtime.Serialization.StreamingContextStates, additional: typing.Any) -> None:
        """Obsoletions.LegacyFormatterMessage"""
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class SerializationException(System.SystemException):
    """This class has no documentation."""

    @overload
    def __init__(self) -> None:
        """
        Creates a new SerializationException with its message
        string set to a default message.
        """
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


class IDeserializationCallback(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class OnDeserializingAttribute(System.Attribute):
    """This class has no documentation."""


class OnSerializedAttribute(System.Attribute):
    """This class has no documentation."""


class IObjectReference(metaclass=abc.ABCMeta):
    """Obsoletions.LegacyFormatterMessage"""


class OptionalFieldAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def VersionAdded(self) -> int:
        ...


class SafeSerializationEventArgs(System.EventArgs):
    """Obsoletions.LegacyFormatterMessage"""

    @property
    def StreamingContext(self) -> System.Runtime.Serialization.StreamingContext:
        ...

    def AddSerializedState(self, serializedState: System.Runtime.Serialization.ISafeSerializationData) -> None:
        ...


class OnSerializingAttribute(System.Attribute):
    """This class has no documentation."""


