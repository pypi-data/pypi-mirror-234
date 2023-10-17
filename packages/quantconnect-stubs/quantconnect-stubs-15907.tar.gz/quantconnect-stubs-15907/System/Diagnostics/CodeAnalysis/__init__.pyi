from typing import overload
import System
import System.Diagnostics.CodeAnalysis


class ConstantExpectedAttribute(System.Attribute):
    """Indicates that the specified method parameter expects a constant."""

    @property
    def Min(self) -> System.Object:
        """Indicates the minimum bound of the expected constant, inclusive."""
        ...

    @property
    def Max(self) -> System.Object:
        """Indicates the maximum bound of the expected constant, inclusive."""
        ...


class ExcludeFromCodeCoverageAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Justification(self) -> str:
        """Gets or sets the justification for excluding the member from code coverage."""
        ...

    def __init__(self) -> None:
        ...


class UnscopedRefAttribute(System.Attribute):
    """Used to indicate a byref escapes and is not scoped."""

    def __init__(self) -> None:
        """Initializes a new instance of the UnscopedRefAttribute class."""
        ...


class SuppressMessageAttribute(System.Attribute):
    """Suppresses reporting of a specific code analysis rule violation, allowing multiple suppressions on a single code artifact. Does not apply to compiler diagnostics."""

    @property
    def Category(self) -> str:
        ...

    @property
    def CheckId(self) -> str:
        ...

    @property
    def Scope(self) -> str:
        ...

    @property
    def Target(self) -> str:
        ...

    @property
    def MessageId(self) -> str:
        ...

    @property
    def Justification(self) -> str:
        ...

    def __init__(self, category: str, checkId: str) -> None:
        ...


class ExperimentalAttribute(System.Attribute):
    """Indicates that an API is experimental and it may change in the future."""

    @property
    def DiagnosticId(self) -> str:
        """Gets the ID that the compiler will use when reporting a use of the API the attribute applies to."""
        ...

    @property
    def UrlFormat(self) -> str:
        """
        Gets or sets the URL for corresponding documentation.
         The API accepts a format string instead of an actual URL, creating a generic URL that includes the diagnostic ID.
        """
        ...

    def __init__(self, diagnosticId: str) -> None:
        """
        Initializes a new instance of the ExperimentalAttribute class, specifying the ID that the compiler will use
         when reporting a use of the API the attribute applies to.
        
        :param diagnosticId: The ID that the compiler will use when reporting a use of the API the attribute applies to.
        """
        ...


