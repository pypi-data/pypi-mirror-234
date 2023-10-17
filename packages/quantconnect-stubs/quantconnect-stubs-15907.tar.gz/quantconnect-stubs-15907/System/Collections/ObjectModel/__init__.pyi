from typing import overload
import abc
import typing

import System
import System.Collections
import System.Collections.Generic
import System.Collections.ObjectModel
import System.Collections.Specialized
import System.ComponentModel

System_Collections_ObjectModel_ReadOnlyCollection_T = typing.TypeVar("System_Collections_ObjectModel_ReadOnlyCollection_T")
System_Collections_ObjectModel_ReadOnlyDictionary_TKey = typing.TypeVar("System_Collections_ObjectModel_ReadOnlyDictionary_TKey")
System_Collections_ObjectModel_ReadOnlyDictionary_TValue = typing.TypeVar("System_Collections_ObjectModel_ReadOnlyDictionary_TValue")
System_Collections_ObjectModel_Collection_T = typing.TypeVar("System_Collections_ObjectModel_Collection_T")
System_Collections_ObjectModel_KeyedCollection_TItem = typing.TypeVar("System_Collections_ObjectModel_KeyedCollection_TItem")
System_Collections_ObjectModel_KeyedCollection_TKey = typing.TypeVar("System_Collections_ObjectModel_KeyedCollection_TKey")
System_Collections_ObjectModel_ObservableCollection_T = typing.TypeVar("System_Collections_ObjectModel_ObservableCollection_T")
System_Collections_ObjectModel_ReadOnlyObservableCollection_T = typing.TypeVar("System_Collections_ObjectModel_ReadOnlyObservableCollection_T")
System_Collections_ObjectModel__EventContainer_Callable = typing.TypeVar("System_Collections_ObjectModel__EventContainer_Callable")
System_Collections_ObjectModel__EventContainer_ReturnType = typing.TypeVar("System_Collections_ObjectModel__EventContainer_ReturnType")


class ReadOnlyCollection(typing.Generic[System_Collections_ObjectModel_ReadOnlyCollection_T], System.Object, System.Collections.Generic.IList[System_Collections_ObjectModel_ReadOnlyCollection_T], System.Collections.IList, System.Collections.Generic.IReadOnlyList[System_Collections_ObjectModel_ReadOnlyCollection_T], typing.Iterable[System_Collections_ObjectModel_ReadOnlyCollection_T]):
    """This class has no documentation."""

    Empty: System.Collections.ObjectModel.ReadOnlyCollection[System_Collections_ObjectModel_ReadOnlyCollection_T]
    """Gets an empty ReadOnlyCollection{T}."""

    @property
    def Count(self) -> int:
        ...

    @property
    def Items(self) -> System.Collections.Generic.IList[System_Collections_ObjectModel_ReadOnlyCollection_T]:
        """This property is protected."""
        ...

    def __getitem__(self, index: int) -> System_Collections_ObjectModel_ReadOnlyCollection_T:
        ...

    def __init__(self, list: System.Collections.Generic.IList[System_Collections_ObjectModel_ReadOnlyCollection_T]) -> None:
        ...

    def Contains(self, value: System_Collections_ObjectModel_ReadOnlyCollection_T) -> bool:
        ...

    def CopyTo(self, array: typing.List[System_Collections_ObjectModel_ReadOnlyCollection_T], index: int) -> None:
        ...

    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System_Collections_ObjectModel_ReadOnlyCollection_T]:
        ...

    def IndexOf(self, value: System_Collections_ObjectModel_ReadOnlyCollection_T) -> int:
        ...


class ReadOnlyDictionary(typing.Generic[System_Collections_ObjectModel_ReadOnlyDictionary_TKey, System_Collections_ObjectModel_ReadOnlyDictionary_TValue], System.Object, System.Collections.Generic.IDictionary[System_Collections_ObjectModel_ReadOnlyDictionary_TKey, System_Collections_ObjectModel_ReadOnlyDictionary_TValue], System.Collections.IDictionary, System.Collections.Generic.IReadOnlyDictionary[System_Collections_ObjectModel_ReadOnlyDictionary_TKey, System_Collections_ObjectModel_ReadOnlyDictionary_TValue], typing.Iterable[System.Collections.Generic.KeyValuePair[System_Collections_ObjectModel_ReadOnlyDictionary_TKey, System_Collections_ObjectModel_ReadOnlyDictionary_TValue]]):
    """This class has no documentation."""

    class KeyCollection(System.Object, System.Collections.Generic.ICollection[System_Collections_ObjectModel_ReadOnlyDictionary_TKey], System.Collections.ICollection, System.Collections.Generic.IReadOnlyCollection[System_Collections_ObjectModel_ReadOnlyDictionary_TKey], typing.Iterable[System_Collections_ObjectModel_ReadOnlyDictionary_TKey]):
        """This class has no documentation."""

        @property
        def Count(self) -> int:
            ...

        def Contains(self, item: System_Collections_ObjectModel_ReadOnlyDictionary_TKey) -> bool:
            ...

        def CopyTo(self, array: typing.List[System_Collections_ObjectModel_ReadOnlyDictionary_TKey], arrayIndex: int) -> None:
            ...

        def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System_Collections_ObjectModel_ReadOnlyDictionary_TKey]:
            ...

    class ValueCollection(System.Object, System.Collections.Generic.ICollection[System_Collections_ObjectModel_ReadOnlyDictionary_TValue], System.Collections.ICollection, System.Collections.Generic.IReadOnlyCollection[System_Collections_ObjectModel_ReadOnlyDictionary_TValue], typing.Iterable[System_Collections_ObjectModel_ReadOnlyDictionary_TValue]):
        """This class has no documentation."""

        @property
        def Count(self) -> int:
            ...

        def CopyTo(self, array: typing.List[System_Collections_ObjectModel_ReadOnlyDictionary_TValue], arrayIndex: int) -> None:
            ...

        def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System_Collections_ObjectModel_ReadOnlyDictionary_TValue]:
            ...

    Empty: System.Collections.ObjectModel.ReadOnlyDictionary[System_Collections_ObjectModel_ReadOnlyDictionary_TKey, System_Collections_ObjectModel_ReadOnlyDictionary_TValue]
    """Gets an empty ReadOnlyDictionary{TKey, TValue}."""

    @property
    def Dictionary(self) -> System.Collections.Generic.IDictionary[System_Collections_ObjectModel_ReadOnlyDictionary_TKey, System_Collections_ObjectModel_ReadOnlyDictionary_TValue]:
        """This property is protected."""
        ...

    @property
    def Keys(self) -> System.Collections.ObjectModel.ReadOnlyDictionary.KeyCollection:
        ...

    @property
    def Values(self) -> System.Collections.ObjectModel.ReadOnlyDictionary.ValueCollection:
        ...

    @property
    def Count(self) -> int:
        ...

    def __getitem__(self, key: System_Collections_ObjectModel_ReadOnlyDictionary_TKey) -> System_Collections_ObjectModel_ReadOnlyDictionary_TValue:
        ...

    def __init__(self, dictionary: System.Collections.Generic.IDictionary[System_Collections_ObjectModel_ReadOnlyDictionary_TKey, System_Collections_ObjectModel_ReadOnlyDictionary_TValue]) -> None:
        ...

    def ContainsKey(self, key: System_Collections_ObjectModel_ReadOnlyDictionary_TKey) -> bool:
        ...

    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System.Collections.Generic.KeyValuePair[System_Collections_ObjectModel_ReadOnlyDictionary_TKey, System_Collections_ObjectModel_ReadOnlyDictionary_TValue]]:
        ...

    def TryGetValue(self, key: System_Collections_ObjectModel_ReadOnlyDictionary_TKey, value: typing.Optional[System_Collections_ObjectModel_ReadOnlyDictionary_TValue]) -> typing.Union[bool, System_Collections_ObjectModel_ReadOnlyDictionary_TValue]:
        ...


class Collection(typing.Generic[System_Collections_ObjectModel_Collection_T], System.Object, System.Collections.Generic.IList[System_Collections_ObjectModel_Collection_T], System.Collections.IList, System.Collections.Generic.IReadOnlyList[System_Collections_ObjectModel_Collection_T], typing.Iterable[System_Collections_ObjectModel_Collection_T]):
    """This class has no documentation."""

    @property
    def Count(self) -> int:
        ...

    @property
    def Items(self) -> System.Collections.Generic.IList[System_Collections_ObjectModel_Collection_T]:
        """This property is protected."""
        ...

    def __getitem__(self, index: int) -> System_Collections_ObjectModel_Collection_T:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, list: System.Collections.Generic.IList[System_Collections_ObjectModel_Collection_T]) -> None:
        ...

    def __setitem__(self, index: int, value: System_Collections_ObjectModel_Collection_T) -> None:
        ...

    def Add(self, item: System_Collections_ObjectModel_Collection_T) -> None:
        ...

    def Clear(self) -> None:
        ...

    def ClearItems(self) -> None:
        """This method is protected."""
        ...

    def Contains(self, item: System_Collections_ObjectModel_Collection_T) -> bool:
        ...

    def CopyTo(self, array: typing.List[System_Collections_ObjectModel_Collection_T], index: int) -> None:
        ...

    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System_Collections_ObjectModel_Collection_T]:
        ...

    def IndexOf(self, item: System_Collections_ObjectModel_Collection_T) -> int:
        ...

    def Insert(self, index: int, item: System_Collections_ObjectModel_Collection_T) -> None:
        ...

    def InsertItem(self, index: int, item: System_Collections_ObjectModel_Collection_T) -> None:
        """This method is protected."""
        ...

    def Remove(self, item: System_Collections_ObjectModel_Collection_T) -> bool:
        ...

    def RemoveAt(self, index: int) -> None:
        ...

    def RemoveItem(self, index: int) -> None:
        """This method is protected."""
        ...

    def SetItem(self, index: int, item: System_Collections_ObjectModel_Collection_T) -> None:
        """This method is protected."""
        ...


class KeyedCollection(typing.Generic[System_Collections_ObjectModel_KeyedCollection_TKey, System_Collections_ObjectModel_KeyedCollection_TItem], System.Collections.ObjectModel.Collection[System_Collections_ObjectModel_KeyedCollection_TItem], metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def Comparer(self) -> System.Collections.Generic.IEqualityComparer[System_Collections_ObjectModel_KeyedCollection_TKey]:
        ...

    @property
    def Dictionary(self) -> System.Collections.Generic.IDictionary[System_Collections_ObjectModel_KeyedCollection_TKey, System_Collections_ObjectModel_KeyedCollection_TItem]:
        """This property is protected."""
        ...

    def __getitem__(self, key: System_Collections_ObjectModel_KeyedCollection_TKey) -> System_Collections_ObjectModel_KeyedCollection_TItem:
        ...

    @overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @overload
    def __init__(self, comparer: System.Collections.Generic.IEqualityComparer[System_Collections_ObjectModel_KeyedCollection_TKey]) -> None:
        """This method is protected."""
        ...

    @overload
    def __init__(self, comparer: System.Collections.Generic.IEqualityComparer[System_Collections_ObjectModel_KeyedCollection_TKey], dictionaryCreationThreshold: int) -> None:
        """This method is protected."""
        ...

    def ChangeItemKey(self, item: System_Collections_ObjectModel_KeyedCollection_TItem, newKey: System_Collections_ObjectModel_KeyedCollection_TKey) -> None:
        """This method is protected."""
        ...

    def ClearItems(self) -> None:
        """This method is protected."""
        ...

    def Contains(self, key: System_Collections_ObjectModel_KeyedCollection_TKey) -> bool:
        ...

    def GetKeyForItem(self, item: System_Collections_ObjectModel_KeyedCollection_TItem) -> System_Collections_ObjectModel_KeyedCollection_TKey:
        """This method is protected."""
        ...

    def InsertItem(self, index: int, item: System_Collections_ObjectModel_KeyedCollection_TItem) -> None:
        """This method is protected."""
        ...

    def Remove(self, key: System_Collections_ObjectModel_KeyedCollection_TKey) -> bool:
        ...

    def RemoveItem(self, index: int) -> None:
        """This method is protected."""
        ...

    def SetItem(self, index: int, item: System_Collections_ObjectModel_KeyedCollection_TItem) -> None:
        """This method is protected."""
        ...

    def TryGetValue(self, key: System_Collections_ObjectModel_KeyedCollection_TKey, item: typing.Optional[System_Collections_ObjectModel_KeyedCollection_TItem]) -> typing.Union[bool, System_Collections_ObjectModel_KeyedCollection_TItem]:
        ...


class ObservableCollection(typing.Generic[System_Collections_ObjectModel_ObservableCollection_T], System.Collections.ObjectModel.Collection[System_Collections_ObjectModel_ObservableCollection_T], System.Collections.Specialized.INotifyCollectionChanged, System.ComponentModel.INotifyPropertyChanged):
    """
    Implementation of a dynamic data collection based on generic Collection<T>,
    implementing INotifyCollectionChanged to notify listeners
    when items get added, removed or the whole list is refreshed.
    """

    @property
    def CollectionChanged(self) -> _EventContainer[typing.Callable[[System.Object, System.Collections.Specialized.NotifyCollectionChangedEventArgs], None], None]:
        """Occurs when the collection changes, either by adding or removing an item."""
        ...

    @property
    def PropertyChanged(self) -> _EventContainer[typing.Callable[[System.Object, System.ComponentModel.PropertyChangedEventArgs], None], None]:
        """
        PropertyChanged event (per INotifyPropertyChanged).
        
        This field is protected.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Initializes a new instance of ObservableCollection that is empty and has default initial capacity."""
        ...

    @overload
    def __init__(self, collection: System.Collections.Generic.IEnumerable[System_Collections_ObjectModel_ObservableCollection_T]) -> None:
        """
        Initializes a new instance of the ObservableCollection class that contains
        elements copied from the specified collection and has sufficient capacity
        to accommodate the number of elements copied.
        
        :param collection: The collection whose elements are copied to the new list.
        """
        ...

    @overload
    def __init__(self, list: System.Collections.Generic.List[System_Collections_ObjectModel_ObservableCollection_T]) -> None:
        """
        Initializes a new instance of the ObservableCollection class
        that contains elements copied from the specified list
        
        :param list: The list whose elements are copied to the new list.
        """
        ...

    def BlockReentrancy(self) -> System.IDisposable:
        """
        Disallow reentrant attempts to change this collection. E.g. an event handler
        of the CollectionChanged event is not allowed to make changes to this collection.
        
        This method is protected.
        """
        ...

    def CheckReentrancy(self) -> None:
        """
        Check and assert for reentrant attempts to change this collection.
        
        This method is protected.
        """
        ...

    def ClearItems(self) -> None:
        """
        Called by base class Collection<T> when the list is being cleared;
        raises a CollectionChanged event to any listeners.
        
        This method is protected.
        """
        ...

    def InsertItem(self, index: int, item: System_Collections_ObjectModel_ObservableCollection_T) -> None:
        """
        Called by base class Collection<T> when an item is added to list;
        raises a CollectionChanged event to any listeners.
        
        This method is protected.
        """
        ...

    def Move(self, oldIndex: int, newIndex: int) -> None:
        """Move item at oldIndex to newIndex."""
        ...

    def MoveItem(self, oldIndex: int, newIndex: int) -> None:
        """
        Called by base class ObservableCollection<T> when an item is to be moved within the list;
        raises a CollectionChanged event to any listeners.
        
        This method is protected.
        """
        ...

    def OnCollectionChanged(self, e: System.Collections.Specialized.NotifyCollectionChangedEventArgs) -> None:
        """
        Raise CollectionChanged event to any listeners.
        Properties/methods modifying this ObservableCollection will raise
        a collection changed event through this virtual method.
        
        This method is protected.
        """
        ...

    def OnPropertyChanged(self, e: System.ComponentModel.PropertyChangedEventArgs) -> None:
        """
        Raises a PropertyChanged event (per INotifyPropertyChanged).
        
        This method is protected.
        """
        ...

    def RemoveItem(self, index: int) -> None:
        """
        Called by base class Collection<T> when an item is removed from list;
        raises a CollectionChanged event to any listeners.
        
        This method is protected.
        """
        ...

    def SetItem(self, index: int, item: System_Collections_ObjectModel_ObservableCollection_T) -> None:
        """
        Called by base class Collection<T> when an item is set in list;
        raises a CollectionChanged event to any listeners.
        
        This method is protected.
        """
        ...


class ReadOnlyObservableCollection(typing.Generic[System_Collections_ObjectModel_ReadOnlyObservableCollection_T], System.Collections.ObjectModel.ReadOnlyCollection[System_Collections_ObjectModel_ReadOnlyObservableCollection_T], System.Collections.Specialized.INotifyCollectionChanged, System.ComponentModel.INotifyPropertyChanged):
    """Read-only wrapper around an ObservableCollection."""

    Empty: System.Collections.ObjectModel.ReadOnlyObservableCollection[System_Collections_ObjectModel_ReadOnlyObservableCollection_T]
    """Gets an empty ReadOnlyObservableCollection{T}."""

    @property
    def CollectionChanged(self) -> _EventContainer[typing.Callable[[System.Object, System.Collections.Specialized.NotifyCollectionChangedEventArgs], None], None]:
        """
        Occurs when the collection changes, either by adding or removing an item.
        
        This field is protected.
        """
        ...

    @property
    def PropertyChanged(self) -> _EventContainer[typing.Callable[[System.Object, System.ComponentModel.PropertyChangedEventArgs], None], None]:
        """
        Occurs when a property changes.
        
        This field is protected.
        """
        ...

    def __init__(self, list: System.Collections.ObjectModel.ObservableCollection[System_Collections_ObjectModel_ReadOnlyObservableCollection_T]) -> None:
        """
        Initializes a new instance of ReadOnlyObservableCollection that
        wraps the given ObservableCollection.
        """
        ...

    def OnCollectionChanged(self, args: System.Collections.Specialized.NotifyCollectionChangedEventArgs) -> None:
        """
        raise CollectionChanged event to any listeners
        
        This method is protected.
        """
        ...

    def OnPropertyChanged(self, args: System.ComponentModel.PropertyChangedEventArgs) -> None:
        """
        raise PropertyChanged event to any listeners
        
        This method is protected.
        """
        ...


class _EventContainer(typing.Generic[System_Collections_ObjectModel__EventContainer_Callable, System_Collections_ObjectModel__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> System_Collections_ObjectModel__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: System_Collections_ObjectModel__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: System_Collections_ObjectModel__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


