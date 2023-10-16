from typing import overload
import abc
import typing

import System
import System.Collections
import System.Globalization
import System.IO
import System.Reflection
import System.Resources
import System.Runtime.Serialization


class UltimateResourceFallbackLocation(System.Enum):
    """Specifies whether a ResourceManager object looks for the resources of the app's default culture in the main assembly or in a satellite assembly."""

    MainAssembly = 0

    Satellite = 1


class IResourceReader(System.Collections.IEnumerable, System.IDisposable, metaclass=abc.ABCMeta):
    """Abstraction to read streams of resources."""


class ResourceReader(System.Object, System.Resources.IResourceReader):
    """This class has no documentation."""

    @overload
    def __init__(self, fileName: str) -> None:
        ...

    @overload
    def __init__(self, stream: System.IO.Stream) -> None:
        ...

    def Close(self) -> None:
        ...

    def Dispose(self) -> None:
        ...

    def GetEnumerator(self) -> System.Collections.IDictionaryEnumerator:
        ...

    def GetResourceData(self, resourceName: str, resourceType: typing.Optional[str], resourceData: typing.Optional[typing.List[int]]) -> typing.Union[None, str, typing.List[int]]:
        ...


class MissingManifestResourceException(System.SystemException):
    """This class has no documentation."""

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
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        This method is protected.
        
        Obsoletions.LegacyFormatterImplMessage
        """
        ...


class NeutralResourcesLanguageAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def CultureName(self) -> str:
        ...

    @property
    def Location(self) -> int:
        """This property contains the int value of a member of the System.Resources.UltimateResourceFallbackLocation enum."""
        ...

    @overload
    def __init__(self, cultureName: str) -> None:
        ...

    @overload
    def __init__(self, cultureName: str, location: System.Resources.UltimateResourceFallbackLocation) -> None:
        ...


class SatelliteContractVersionAttribute(System.Attribute):
    """Instructs a ResourceManager object to ask for a particular version of a satellite assembly."""

    @property
    def Version(self) -> str:
        ...

    def __init__(self, version: str) -> None:
        ...


class MissingSatelliteAssemblyException(System.SystemException):
    """The exception that is thrown when the satellite assembly for the resources of the default culture is missing."""

    @property
    def CultureName(self) -> str:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, cultureName: str) -> None:
        ...

    @overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...

    @overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        This method is protected.
        
        Obsoletions.LegacyFormatterImplMessage
        """
        ...


class ResourceSet(System.Object, System.IDisposable, System.Collections.IEnumerable):
    """This class has no documentation."""

    @property
    def Reader(self) -> System.Resources.IResourceReader:
        """This field is protected."""
        ...

    @overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @overload
    def __init__(self, fileName: str) -> None:
        ...

    @overload
    def __init__(self, stream: System.IO.Stream) -> None:
        ...

    @overload
    def __init__(self, reader: System.Resources.IResourceReader) -> None:
        ...

    def Close(self) -> None:
        ...

    @overload
    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    @overload
    def Dispose(self) -> None:
        ...

    def GetDefaultReader(self) -> typing.Type:
        ...

    def GetDefaultWriter(self) -> typing.Type:
        ...

    def GetEnumerator(self) -> System.Collections.IDictionaryEnumerator:
        ...

    @overload
    def GetObject(self, name: str) -> System.Object:
        ...

    @overload
    def GetObject(self, name: str, ignoreCase: bool) -> System.Object:
        ...

    @overload
    def GetString(self, name: str) -> str:
        ...

    @overload
    def GetString(self, name: str, ignoreCase: bool) -> str:
        ...

    def ReadResources(self) -> None:
        """This method is protected."""
        ...


class ResourceManager(System.Object):
    """This class has no documentation."""

    @property
    def BaseNameField(self) -> str:
        """This field is protected."""
        ...

    @property
    def MainAssembly(self) -> System.Reflection.Assembly:
        """This field is protected."""
        ...

    MagicNumber: int = ...

    HeaderVersionNumber: int = 1

    @property
    def BaseName(self) -> str:
        ...

    @property
    def IgnoreCase(self) -> bool:
        ...

    @property
    def ResourceSetType(self) -> typing.Type:
        ...

    @property
    def FallbackLocation(self) -> int:
        """
        This property contains the int value of a member of the System.Resources.UltimateResourceFallbackLocation enum.
        
        This property is protected.
        """
        ...

    @overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @overload
    def __init__(self, baseName: str, assembly: System.Reflection.Assembly) -> None:
        ...

    @overload
    def __init__(self, baseName: str, assembly: System.Reflection.Assembly, usingResourceSet: typing.Type) -> None:
        ...

    @overload
    def __init__(self, resourceSource: typing.Type) -> None:
        ...

    @staticmethod
    def CreateFileBasedResourceManager(baseName: str, resourceDir: str, usingResourceSet: typing.Type) -> System.Resources.ResourceManager:
        ...

    @staticmethod
    def GetNeutralResourcesLanguage(a: System.Reflection.Assembly) -> System.Globalization.CultureInfo:
        """This method is protected."""
        ...

    @overload
    def GetObject(self, name: str) -> System.Object:
        ...

    @overload
    def GetObject(self, name: str, culture: System.Globalization.CultureInfo) -> System.Object:
        ...

    def GetResourceFileName(self, culture: System.Globalization.CultureInfo) -> str:
        """This method is protected."""
        ...

    def GetResourceSet(self, culture: System.Globalization.CultureInfo, createIfNotExists: bool, tryParents: bool) -> System.Resources.ResourceSet:
        ...

    @staticmethod
    def GetSatelliteContractVersion(a: System.Reflection.Assembly) -> System.Version:
        """This method is protected."""
        ...

    @overload
    def GetStream(self, name: str) -> System.IO.UnmanagedMemoryStream:
        ...

    @overload
    def GetStream(self, name: str, culture: System.Globalization.CultureInfo) -> System.IO.UnmanagedMemoryStream:
        ...

    @overload
    def GetString(self, name: str) -> str:
        ...

    @overload
    def GetString(self, name: str, culture: System.Globalization.CultureInfo) -> str:
        ...

    def InternalGetResourceSet(self, culture: System.Globalization.CultureInfo, createIfNotExists: bool, tryParents: bool) -> System.Resources.ResourceSet:
        """This method is protected."""
        ...

    def ReleaseAllResources(self) -> None:
        ...


