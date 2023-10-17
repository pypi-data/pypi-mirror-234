from typing import overload
import abc
import typing

import System.Windows.Input

System_Windows_Input__EventContainer_Callable = typing.TypeVar("System_Windows_Input__EventContainer_Callable")
System_Windows_Input__EventContainer_ReturnType = typing.TypeVar("System_Windows_Input__EventContainer_ReturnType")


class ICommand(metaclass=abc.ABCMeta):
    """An interface that allows an application author to define a method to be invoked."""


class _EventContainer(typing.Generic[System_Windows_Input__EventContainer_Callable, System_Windows_Input__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> System_Windows_Input__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: System_Windows_Input__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: System_Windows_Input__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


