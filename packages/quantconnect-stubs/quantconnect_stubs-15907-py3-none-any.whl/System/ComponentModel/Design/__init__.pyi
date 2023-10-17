from typing import overload
import abc
import typing

import System
import System.Collections
import System.ComponentModel
import System.ComponentModel.Design
import System.IO
import System.Reflection
import System.Runtime.InteropServices
import System.Runtime.Serialization

IServiceProvider = typing.Any

System_ComponentModel_Design__EventContainer_Callable = typing.TypeVar("System_ComponentModel_Design__EventContainer_Callable")
System_ComponentModel_Design__EventContainer_ReturnType = typing.TypeVar("System_ComponentModel_Design__EventContainer_ReturnType")


class TypeDescriptionProviderService(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @overload
    def GetProvider(self, instance: typing.Any) -> System.ComponentModel.TypeDescriptionProvider:
        ...

    @overload
    def GetProvider(self, type: typing.Type) -> System.ComponentModel.TypeDescriptionProvider:
        ...


class ComponentChangedEventArgs(System.EventArgs):
    """Provides data for the System.ComponentModel.Design.IComponentChangeService.ComponentChanged event."""

    @property
    def Component(self) -> System.Object:
        """Gets or sets the component that is the cause of this event."""
        ...

    @property
    def Member(self) -> System.ComponentModel.MemberDescriptor:
        """Gets or sets the member that is about to change."""
        ...

    @property
    def NewValue(self) -> System.Object:
        """Gets or sets the new value of the changed member."""
        ...

    @property
    def OldValue(self) -> System.Object:
        """Gets or sets the old value of the changed member."""
        ...

    def __init__(self, component: typing.Any, member: System.ComponentModel.MemberDescriptor, oldValue: typing.Any, newValue: typing.Any) -> None:
        """Initializes a new instance of the System.ComponentModel.Design.ComponentChangedEventArgs class."""
        ...


class IInheritanceService(metaclass=abc.ABCMeta):
    """Provides a set of utilities for analyzing and identifying inherited components."""


class IEventBindingService(metaclass=abc.ABCMeta):
    """Provides a set of useful methods for binding System.ComponentModel.EventDescriptor objects to user code."""


class IDesignerHostTransactionState(metaclass=abc.ABCMeta):
    """Methods for the Designer host to report on the state of transactions."""


class HelpContextType(System.Enum):
    """This class has no documentation."""

    Ambient = 0

    Window = 1

    Selection = 2

    ToolWindowSelection = 3


class ITypeDescriptorFilterService(metaclass=abc.ABCMeta):
    """Modifies the set of type descriptors that a component provides."""


class IExtenderProviderService(metaclass=abc.ABCMeta):
    """Provides an interface to add and remove extender providers."""


class HelpKeywordType(System.Enum):
    """Specifies identifiers that can be used to indicate the type of a help keyword."""

    F1Keyword = 0
    """Indicates the keyword is a word F1 was pressed to request help regarding."""

    GeneralKeyword = 1
    """Indicates the keyword is a general keyword."""

    FilterKeyword = 2
    """Indicates the keyword is a filter keyword."""


class CommandID(System.Object):
    """
    Represents a numeric Command ID and globally unique ID (GUID) menu
    identifier that together uniquely identify a command.
    """

    @property
    def ID(self) -> int:
        """Gets or sets the numeric command ID."""
        ...

    @property
    def Guid(self) -> System.Guid:
        """
        Gets or sets the globally unique ID (GUID) of the menu group that the
        menu command this CommandID represents belongs to.
        """
        ...

    def __init__(self, menuGroup: System.Guid, commandID: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.Design.CommandID
        class. Creates a new command ID.
        """
        ...

    def Equals(self, obj: typing.Any) -> bool:
        """Overrides Object's Equals method."""
        ...

    def GetHashCode(self) -> int:
        ...

    def ToString(self) -> str:
        """Overrides Object's ToString method."""
        ...


class StandardCommands(System.Object):
    """
    Specifies identifiers for the standard set of commands that are available to
    most applications.
    """

    AlignBottom: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the AlignBottom command. Read only."""

    AlignHorizontalCenters: System.ComponentModel.Design.CommandID = ...
    """
    Gets the GUID/integer value pair for the AlignHorizontalCenters command. Read
    only.
    """

    AlignLeft: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the AlignLeft command. Read only."""

    AlignRight: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the AlignRight command. Read only."""

    AlignToGrid: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the AlignToGrid command. Read only."""

    AlignTop: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the AlignTop command. Read only."""

    AlignVerticalCenters: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the AlignVerticalCenters command. Read only."""

    ArrangeBottom: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the ArrangeBottom command. Read only."""

    ArrangeRight: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the ArrangeRight command. Read only."""

    BringForward: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the BringForward command. Read only."""

    BringToFront: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the BringToFront command. Read only."""

    CenterHorizontally: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the CenterHorizontally command. Read only."""

    CenterVertically: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the CenterVertically command. Read only."""

    ViewCode: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the Code command. Read only."""

    DocumentOutline: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the DocumentOutline command. Read only."""

    Copy: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the Copy command. Read only."""

    Cut: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the Cut command. Read only."""

    Delete: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the Delete command. Read only."""

    Group: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the Group command. Read only."""

    HorizSpaceConcatenate: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the HorizSpaceConcatenate command. Read only."""

    HorizSpaceDecrease: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the HorizSpaceDecrease command. Read only."""

    HorizSpaceIncrease: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the HorizSpaceIncrease command. Read only."""

    HorizSpaceMakeEqual: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the HorizSpaceMakeEqual command. Read only."""

    Paste: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the Paste command. Read only."""

    Properties: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the Properties command. Read only."""

    Redo: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the Redo command. Read only."""

    MultiLevelRedo: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the MultiLevelRedo command. Read only."""

    SelectAll: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the SelectAll command. Read only."""

    SendBackward: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the SendBackward command. Read only."""

    SendToBack: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the SendToBack command. Read only."""

    SizeToControl: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the SizeToControl command. Read only."""

    SizeToControlHeight: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the SizeToControlHeight command. Read only."""

    SizeToControlWidth: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the SizeToControlWidth command. Read only."""

    SizeToFit: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the SizeToFit command. Read only."""

    SizeToGrid: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the SizeToGrid command. Read only."""

    SnapToGrid: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the SnapToGrid command. Read only."""

    TabOrder: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the TabOrder command. Read only."""

    Undo: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the Undo command. Read only."""

    MultiLevelUndo: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the MultiLevelUndo command. Read only."""

    Ungroup: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the Ungroup command. Read only."""

    VertSpaceConcatenate: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the VertSpaceConcatenate command. Read only."""

    VertSpaceDecrease: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the VertSpaceDecrease command. Read only."""

    VertSpaceIncrease: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the VertSpaceIncrease command. Read only."""

    VertSpaceMakeEqual: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the VertSpaceMakeEqual command. Read only."""

    ShowGrid: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the ShowGrid command. Read only."""

    ViewGrid: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the ViewGrid command. Read only."""

    Replace: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the Replace command. Read only."""

    PropertiesWindow: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the PropertiesWindow command. Read only."""

    LockControls: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the LockControls command. Read only."""

    F1Help: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the F1Help command. Read only."""

    ArrangeIcons: System.ComponentModel.Design.CommandID = ...

    LineupIcons: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the LineupIcons command. Read only."""

    ShowLargeIcons: System.ComponentModel.Design.CommandID = ...
    """Gets the GUID/integer value pair for the ShowLargeIcons command. Read only."""

    VerbFirst: System.ComponentModel.Design.CommandID = ...
    """Gets the first of a set of verbs. Read only."""

    VerbLast: System.ComponentModel.Design.CommandID = ...
    """Gets the last of a set of verbs.Read only."""


class IDesignerEventService(metaclass=abc.ABCMeta):
    """Provides global event notifications and the ability to create designers."""


class HelpKeywordAttribute(System.Attribute):
    """
    Allows specification of the context keyword that will be specified for this class or member. By default,
    the help keyword for a class is the Type's full name, and for a member it's the full name of the type that declared the property,
    plus the property name itself.
    
    For example, consider System.Windows.Forms.Button and it's Text property:
    
    The class keyword is "System.Windows.Forms.Button", but the Text property keyword is "System.Windows.Forms.Control.Text", because the Text
    property is declared on the System.Windows.Forms.Control class rather than the Button class itself; the Button class inherits the property.
    By contrast, the DialogResult property is declared on the Button so its keyword would be "System.Windows.Forms.Button.DialogResult".
    
    When the help system gets the keywords, it will first look at this attribute. At the class level, it will return the string specified by the
    HelpContextAttribute. Note this will not be used for members of the Type in question. They will still reflect the declaring Type's actual
    full name, plus the member name. To override this, place the attribute on the member itself.
    
    Example:
    
    [HelpKeywordAttribute(typeof(Component))]
    public class MyComponent : Component {
    
    
    public string Property1 { get{return "";};
    
    [HelpKeywordAttribute("SomeNamespace.SomeOtherClass.Property2")]
    public string Property2 { get{return "";};
    
    }
    
    
    For the above class (default without attribution):
    
    Class keyword: "System.ComponentModel.Component" ("MyNamespace.MyComponent')
    Property1 keyword: "MyNamespace.MyComponent.Property1" (default)
    Property2 keyword: "SomeNamespace.SomeOtherClass.Property2" ("MyNamespace.MyComponent.Property2")
    """

    Default: System.ComponentModel.Design.HelpKeywordAttribute = ...
    """Default value for HelpKeywordAttribute, which is null."""

    @property
    def HelpKeyword(self) -> str:
        """Retrieves the HelpKeyword this attribute supplies."""
        ...

    @overload
    def __init__(self) -> None:
        """Default constructor, which creates an attribute with a null HelpKeyword."""
        ...

    @overload
    def __init__(self, keyword: str) -> None:
        """Creates a HelpKeywordAttribute with the value being the given keyword string."""
        ...

    @overload
    def __init__(self, t: typing.Type) -> None:
        """Creates a HelpKeywordAttribute with the value being the full name of the given type."""
        ...

    def Equals(self, obj: typing.Any) -> bool:
        """Two instances of a HelpKeywordAttribute are equal if they're HelpKeywords are equal."""
        ...

    def GetHashCode(self) -> int:
        """"""
        ...

    def IsDefaultAttribute(self) -> bool:
        """Returns true if this Attribute's HelpKeyword is null."""
        ...


class SelectionTypes(System.Enum):
    """
    Specifies identifiers that indicate the type of selection for a component or
    group of components that are selected.
    """

    Auto = ...
    """
    A Normal selection. With this type of selection, the selection service responds
    to the control and shift keys to support appending or toggling components into the
    selection as needed.
    """

    Normal = ...
    """
    A Normal selection. With this type of selection, the selection service responds
    to the control and shift keys to support appending or toggling components into the
    selection as needed.
    
    SelectionTypes.Normal has been deprecated. Use SelectionTypes.Auto instead.
    """

    Replace = ...
    """
    A Replace selection. This causes the selection service to always replace the
    current selection with the replacement.
    """

    MouseDown = ...
    """
    A MouseDown selection. Happens when the user presses down on
    the mouse button when the pointer is over a control (or component). If a
    component in the selection list is already selected, it does not remove the
    existing selection, but promotes that component to be the primary selection.
    
    SelectionTypes.MouseDown has been deprecated and is not supported.
    """

    MouseUp = ...
    """
    A MouseUp selection. Happens when the user releases the
    mouse button when a control (or component) has been selected. If a component
    in the selection list is already selected, it does not remove the
    existing selection, but promotes that component to be the primary selection.
    
    SelectionTypes.MouseUp has been deprecated and is not supported.
    """

    Click = ...
    """
    A Click selection.
    Happens when a user clicks on a component. If a component in the selection list is already
    selected, it does not remove the existing selection, but promotes that component to be the
    primary selection.
    
    SelectionTypes.Click has been deprecated. Use SelectionTypes.Primary instead.
    """

    Primary = ...
    """
    A Primary selection.
    Happens when a user clicks on a component. If a component in the selection list is already
    selected, it does not remove the existing selection, but promotes that component to be the
    primary selection.
    """

    Toggle = ...
    """
    A toggle selection.
    This selection toggles the current selection with the provided selection. So, if
    a component is already selected and is passed into SetSelectedComponents with a
    selection type of Toggle, it will be unselected.
    """

    Add = ...
    """
    An Add selection.
    This selection adds the selected components to the current selection,
    maintaining the current set of selected components.
    """

    Remove = ...
    """
    A Remove selection.
    This selection removes the selected components from the current selection,
    maintaining the current set of selected components.
    """

    Valid = ...
    """
    Limits valid selection types to Normal, Replace, MouseDown, MouseUp,
    Click, Toggle or Add.
    
    SelectionTypes.Valid has been deprecated. Use Enum class methods to determine valid values, or use a type converter instead.
    """


class MenuCommand(System.Object):
    """Represents a Windows menu or toolbar item."""

    @property
    def Checked(self) -> bool:
        """Gets or sets a value indicating whether this menu item is checked."""
        ...

    @property
    def Enabled(self) -> bool:
        """Gets or sets a value indicating whether this menu item is available."""
        ...

    @property
    def Properties(self) -> System.Collections.IDictionary:
        ...

    @property
    def Supported(self) -> bool:
        """Gets or sets a value indicating whether this menu item is supported."""
        ...

    @property
    def Visible(self) -> bool:
        """Gets or sets a value indicating if this menu item is visible."""
        ...

    @property
    def CommandChanged(self) -> _EventContainer[typing.Callable[[System.Object, System.EventArgs], None], None]:
        """Occurs when the menu command changes."""
        ...

    @property
    def CommandID(self) -> System.ComponentModel.Design.CommandID:
        """Gets the System.ComponentModel.Design.CommandID associated with this menu command."""
        ...

    @property
    def OleStatus(self) -> int:
        """Gets the OLE command status code for this menu item."""
        ...

    def __init__(self, handler: typing.Callable[[System.Object, System.EventArgs], None], command: System.ComponentModel.Design.CommandID) -> None:
        """Initializes a new instance of System.ComponentModel.Design.MenuCommand."""
        ...

    @overload
    def Invoke(self) -> None:
        """Invokes a menu item."""
        ...

    @overload
    def Invoke(self, arg: typing.Any) -> None:
        """
        Invokes a menu item. The default implementation of this method ignores
        the argument, but deriving classes may override this method.
        """
        ...

    def OnCommandChanged(self, e: System.EventArgs) -> None:
        """
        Provides notification and is called in response to
        a System.ComponentModel.Design.MenuCommand.CommandChanged event.
        
        This method is protected.
        """
        ...

    def ToString(self) -> str:
        """Overrides object's ToString()."""
        ...


class DesignerVerb(System.ComponentModel.Design.MenuCommand):
    """Represents a verb that can be executed by a component's designer."""

    @property
    def Description(self) -> str:
        """Gets or sets the description of the menu item for the verb."""
        ...

    @property
    def Text(self) -> str:
        """Gets or sets the text to show on the menu item for the verb."""
        ...

    @overload
    def __init__(self, text: str, handler: typing.Callable[[System.Object, System.EventArgs], None]) -> None:
        """Initializes a new instance of the System.ComponentModel.Design.DesignerVerb class."""
        ...

    @overload
    def __init__(self, text: str, handler: typing.Callable[[System.Object, System.EventArgs], None], startCommandID: System.ComponentModel.Design.CommandID) -> None:
        """
        Initializes a new instance of the System.ComponentModel.Design.DesignerVerb
        class.
        """
        ...

    def ToString(self) -> str:
        """Overrides object's ToString()."""
        ...


class IServiceContainer(IServiceProvider, metaclass=abc.ABCMeta):
    """
    This interface provides a container for services. A service container
    is, by definition, a service provider. In addition to providing services
    it also provides a mechanism for adding and removing services.
    """


class IDesignerHost(System.ComponentModel.Design.IServiceContainer, metaclass=abc.ABCMeta):
    """
    Provides methods to adjust the configuration of and retrieve
    information about the services and behavior of a designer.
    """


class DesignerEventArgs(System.EventArgs):
    """
    Provides data for the System.ComponentModel.Design.IDesignerEventService.DesignerEvent
    event that is generated when a document is created or disposed.
    """

    @property
    def Designer(self) -> System.ComponentModel.Design.IDesignerHost:
        """Gets or sets the host of the document."""
        ...

    def __init__(self, host: System.ComponentModel.Design.IDesignerHost) -> None:
        """
        Initializes a new instance of the System.ComponentModel.Design.DesignerEventArgs
        class.
        """
        ...


class IComponentDiscoveryService(metaclass=abc.ABCMeta):
    """
    This service allows design-time enumeration of components across the toolbox
    and other available types at design-time.
    """


class ComponentChangingEventArgs(System.EventArgs):
    """Provides data for the System.ComponentModel.Design.IComponentChangeService.ComponentChanging event."""

    @property
    def Component(self) -> System.Object:
        """Gets or sets the component that is being changed or that is the parent container of the member being changed."""
        ...

    @property
    def Member(self) -> System.ComponentModel.MemberDescriptor:
        """Gets or sets the member of the component that is about to be changed."""
        ...

    def __init__(self, component: typing.Any, member: System.ComponentModel.MemberDescriptor) -> None:
        """Initializes a new instance of the System.ComponentModel.Design.ComponentChangingEventArgs class."""
        ...


class ITypeDiscoveryService(metaclass=abc.ABCMeta):
    """
    The type discovery service is used to discover available types at design time,
    when the consumer doesn't know the names of existing types or referenced assemblies.
    """


class ViewTechnology(System.Enum):
    """Specifies a set of technologies designer hosts should support."""

    Passthrough = 0
    """
    Specifies that the view for a root designer is defined by some
    private interface contract between the designer and the
    development environment. This implies a tight coupling
    between the development environment and the designer, and should
    be avoided. This does allow older COM2 technologies to
    be shown in development environments that support
    COM2 interface technologies such as doc objects and ActiveX
    controls.
    
    ViewTechnology.Passthrough has been deprecated. Use ViewTechnology.Default instead.
    """

    WindowsForms = 1
    """
    Specifies that the view for a root designer is supplied through
    a Windows Forms control object. The designer host will fill the
    development environment's document window with this control.
    
    ViewTechnology.WindowsForms has been deprecated. Use ViewTechnology.Default instead.
    """

    Default = 2
    """
    Specifies the default view technology support. Here, the root designer may return
    any type of object it wishes, but it must be an object that can be "fitted" with
    an adapter to the technology of the host. Hosting environments such as Visual
    Studio will provide a way to plug in new view technology adapters. The default
    view object for the Windows Forms designer is a Control instance, while the
    default view object for the Avalon designer is an Element instance.
    """


class DesignerCollection(System.Object, System.Collections.ICollection):
    """Provides a read-only collection of documents."""

    @property
    def Count(self) -> int:
        """Gets or sets the number of documents in the collection."""
        ...

    def __getitem__(self, index: int) -> System.ComponentModel.Design.IDesignerHost:
        """Gets or sets the document at the specified index."""
        ...

    @overload
    def __init__(self, designers: typing.List[System.ComponentModel.Design.IDesignerHost]) -> None:
        """
        Initializes a new instance of the System.ComponentModel.Design.DesignerCollection class
        that stores an array with a pointer to each System.ComponentModel.Design.IDesignerHost
        for each document in the collection.
        """
        ...

    @overload
    def __init__(self, designers: System.Collections.IList) -> None:
        """
        Initializes a new instance of the System.ComponentModel.Design.DesignerCollection class
        that stores an array with a pointer to each System.ComponentModel.Design.IDesignerHost
        for each document in the collection.
        """
        ...

    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """Creates and retrieves a new enumerator for this collection."""
        ...


class DesigntimeLicenseContext(System.ComponentModel.LicenseContext):
    """Provides design-time support for licensing."""

    @property
    def UsageMode(self) -> int:
        """
        Gets or sets the license usage mode.
        
        This property contains the int value of a member of the System.ComponentModel.LicenseUsageMode enum.
        """
        ...

    def GetSavedLicenseKey(self, type: typing.Type, resourceAssembly: System.Reflection.Assembly) -> str:
        """Gets a saved license key."""
        ...

    def SetSavedLicenseKey(self, type: typing.Type, key: str) -> None:
        """Sets a saved license key."""
        ...


class IResourceService(metaclass=abc.ABCMeta):
    """Provides designers a way to access a resource for the current design-time object."""


class IDesignerFilter(metaclass=abc.ABCMeta):
    """
    Provides access to, and an interface for filtering, the dictionaries that store the
    properties, attributes, or events of a component.
    """


class ITypeResolutionService(metaclass=abc.ABCMeta):
    """The type resolution service is used to load types at design time."""


class IExtenderListService(metaclass=abc.ABCMeta):
    """Provides an interface to list extender providers."""


class IDesignerOptionService(metaclass=abc.ABCMeta):
    """Provides access to get and set option values for a designer."""


class ServiceContainer(System.Object, System.ComponentModel.Design.IServiceContainer, System.IDisposable):
    """This is a simple implementation of IServiceContainer."""

    @property
    def DefaultServices(self) -> typing.List[typing.Type]:
        """
        This property returns the default services that are implemented directly on this IServiceContainer.
        the default implementation of this property is to return the IServiceContainer and ServiceContainer
        types. You may override this property and return your own types, modifying the default behavior
        of GetService.
        
        This property is protected.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Creates a new service object container."""
        ...

    @overload
    def __init__(self, parentProvider: typing.Optional[IServiceProvider]) -> None:
        """Creates a new service object container."""
        ...

    @overload
    def AddService(self, serviceType: typing.Type, serviceInstance: typing.Any) -> None:
        """Adds the given service to the service container."""
        ...

    @overload
    def AddService(self, serviceType: typing.Type, serviceInstance: typing.Any, promote: bool) -> None:
        """Adds the given service to the service container."""
        ...

    @overload
    def AddService(self, serviceType: typing.Type, callback: typing.Callable[[System.ComponentModel.Design.IServiceContainer, typing.Type], System.Object]) -> None:
        """Adds the given service to the service container."""
        ...

    @overload
    def AddService(self, serviceType: typing.Type, callback: typing.Callable[[System.ComponentModel.Design.IServiceContainer, typing.Type], System.Object], promote: bool) -> None:
        """Adds the given service to the service container."""
        ...

    @overload
    def Dispose(self) -> None:
        """
        Disposes this service container. This also walks all instantiated services within the container
        and disposes any that implement IDisposable, and clears the service list.
        """
        ...

    @overload
    def Dispose(self, disposing: bool) -> None:
        """
        Disposes this service container. This also walks all instantiated services within the container
        and disposes any that implement IDisposable, and clears the service list.
        
        This method is protected.
        """
        ...

    def GetService(self, serviceType: typing.Type) -> System.Object:
        """Retrieves the requested service."""
        ...

    @overload
    def RemoveService(self, serviceType: typing.Type) -> None:
        """Removes the given service type from the service container."""
        ...

    @overload
    def RemoveService(self, serviceType: typing.Type, promote: bool) -> None:
        """Removes the given service type from the service container."""
        ...


class StandardToolWindows(System.Object):
    """
    Defines GUID specifiers that contain GUIDs which reference the standard set of tool windows that are available in
    the design environment.
    """

    ObjectBrowser: System.Guid = ...
    """Gets the GUID for the object browser."""

    OutputWindow: System.Guid = ...
    """Gets the GUID for the output window."""

    ProjectExplorer: System.Guid = ...
    """Gets the GUID for the project explorer."""

    PropertyBrowser: System.Guid = ...
    """Gets the GUID for the properties window."""

    RelatedLinks: System.Guid = ...
    """Gets the GUID for the related links frame."""

    ServerExplorer: System.Guid = ...
    """Gets the GUID for the server explorer."""

    TaskList: System.Guid = ...
    """Gets the GUID for the task list."""

    Toolbox: System.Guid = ...
    """Gets the GUID for the toolbox."""


class IComponentInitializer(metaclass=abc.ABCMeta):
    """
    IComponentInitializer can be implemented on an object that also implements IDesigner.
    This interface allows a newly created component to be given some stock default values,
    such as a caption, default size, or other values. Recommended default values for
    the component's properties are passed in as a dictionary.
    """


class DesignerTransactionCloseEventArgs(System.EventArgs):
    """This class has no documentation."""

    @property
    def TransactionCommitted(self) -> bool:
        ...

    @property
    def LastTransaction(self) -> bool:
        ...

    @overload
    def __init__(self, commit: bool, lastTransaction: bool) -> None:
        """
        Creates a new event args. Commit is true if the transaction is committed, and
        lastTransaction is true if this is the last transaction to close.
        """
        ...

    @overload
    def __init__(self, commit: bool) -> None:
        """
        Creates a new event args. Commit is true if the transaction is committed. This
        defaults the LastTransaction property to true.
        
        This constructor has been deprecated. Use DesignerTransactionCloseEventArgs(bool, bool) instead.
        """
        ...


class IHelpService(metaclass=abc.ABCMeta):
    """
    Provides the Integrated Development Environment (IDE) help
    system with contextual information for the current task.
    """


class DesigntimeLicenseContextSerializer(System.Object):
    """Provides support for design-time license context serialization."""

    @staticmethod
    def Serialize(o: System.IO.Stream, cryptoKey: str, context: System.ComponentModel.Design.DesigntimeLicenseContext) -> None:
        """
        Serializes the licenses within the specified design-time license context
        using the specified key and output stream.
        """
        ...


class IReferenceService(metaclass=abc.ABCMeta):
    """
    Provides an interface to get names and references to objects. These
    methods can search using the specified name or reference.
    """


class IComponentChangeService(metaclass=abc.ABCMeta):
    """Provides an interface to add and remove the event handlers for System.ComponentModel.Design.IComponentChangeService.ComponentAdded, System.ComponentModel.Design.IComponentChangeService.ComponentAdding, System.ComponentModel.Design.IComponentChangeService.ComponentChanged, System.ComponentModel.Design.IComponentChangeService.ComponentChanging, System.ComponentModel.Design.IComponentChangeService.ComponentRemoved, System.ComponentModel.Design.IComponentChangeService.ComponentRemoving, and System.ComponentModel.Design.IComponentChangeService.ComponentRename events."""


class ComponentRenameEventArgs(System.EventArgs):
    """Provides data for the System.ComponentModel.Design.IComponentChangeService.ComponentRename event."""

    @property
    def Component(self) -> System.Object:
        """Gets or sets the component that is being renamed."""
        ...

    @property
    def OldName(self) -> str:
        """Gets or sets the name of the component before the rename."""
        ...

    @property
    def NewName(self) -> str:
        """Gets or sets the current name of the component."""
        ...

    def __init__(self, component: typing.Any, oldName: str, newName: str) -> None:
        """
        Initializes a new instance of the System.ComponentModel.Design.ComponentRenameEventArgs
        class.
        """
        ...


class IDesigner(System.IDisposable, metaclass=abc.ABCMeta):
    """
    Provides the basic framework for building a custom designer.
    This interface stores the verbs available to the designer, as well as basic
    services for the designer.
    """


class ITreeDesigner(System.ComponentModel.Design.IDesigner, metaclass=abc.ABCMeta):
    """
    ITreeDesigner is a variation of IDesigner that provides support for
    generically indicating parent / child relationships within a designer.
    """


class ActiveDesignerEventArgs(System.EventArgs):
    """
    Provides data for the System.ComponentModel.Design.IDesignerEventService.ActiveDesigner
    event.
    """

    @property
    def OldDesigner(self) -> System.ComponentModel.Design.IDesignerHost:
        """Gets or sets the document that is losing activation."""
        ...

    @property
    def NewDesigner(self) -> System.ComponentModel.Design.IDesignerHost:
        """Gets or sets the document that is gaining activation."""
        ...

    def __init__(self, oldDesigner: System.ComponentModel.Design.IDesignerHost, newDesigner: System.ComponentModel.Design.IDesignerHost) -> None:
        """
        Initializes a new instance of the System.ComponentModel.Design.ActiveDesignerEventArgs
        class.
        """
        ...


class DesignerTransaction(System.Object, System.IDisposable, metaclass=abc.ABCMeta):
    """
    Identifies a transaction within a designer. Transactions are
    used to wrap several changes into one unit of work, which
    helps performance.
    """

    @property
    def Canceled(self) -> bool:
        ...

    @property
    def Committed(self) -> bool:
        ...

    @property
    def Description(self) -> str:
        ...

    @overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @overload
    def __init__(self, description: str) -> None:
        """This method is protected."""
        ...

    def Cancel(self) -> None:
        ...

    def Commit(self) -> None:
        """
        Commits this transaction. Once a transaction has been committed, further
        calls to this method will do nothing. You should always call this method
        after creating a transaction to ensure that the transaction is closed properly.
        """
        ...

    def Dispose(self, disposing: bool) -> None:
        """This method is protected."""
        ...

    def OnCancel(self) -> None:
        """
        User code should implement this method to perform the actual work of
        committing a transaction.
        
        This method is protected.
        """
        ...

    def OnCommit(self) -> None:
        """
        User code should implement this method to perform the actual work of
        committing a transaction.
        
        This method is protected.
        """
        ...


class DesignerOptionService(System.Object, System.ComponentModel.Design.IDesignerOptionService, metaclass=abc.ABCMeta):
    """Provides access to get and set option values for a designer."""

    class DesignerOptionCollection(System.Object, System.Collections.IList):
        """
        The DesignerOptionCollection class is a collection that contains
        other DesignerOptionCollection objects. This forms a tree of options,
        with each branch of the tree having a name and a possible collection of
        properties. Each parent branch of the tree contains a union of the
        properties if all the branch's children.
        """

        @property
        def Count(self) -> int:
            """The count of child options collections this collection contains."""
            ...

        @property
        def Name(self) -> str:
            """
            The name of this collection. Names are programmatic names and are not
            localized. A name search is case insensitive.
            """
            ...

        @property
        def Parent(self) -> System.ComponentModel.Design.DesignerOptionService.DesignerOptionCollection:
            """Returns the parent collection object, or null if there is no parent."""
            ...

        @property
        def Properties(self) -> System.ComponentModel.PropertyDescriptorCollection:
            """
            The collection of properties that this OptionCollection, along with all of
            its children, offers. PropertyDescriptors are taken directly from the
            value passed to CreateObjectCollection and wrapped in an additional property
            descriptor that hides the value object from the user. This means that any
            value may be passed into the "component" parameter of the various
            PropertyDescriptor methods. The value is ignored and is replaced with
            the correct value internally.
            """
            ...

        @overload
        def __getitem__(self, index: int) -> System.ComponentModel.Design.DesignerOptionService.DesignerOptionCollection:
            """Retrieves the child collection at the given index."""
            ...

        @overload
        def __getitem__(self, name: str) -> System.ComponentModel.Design.DesignerOptionService.DesignerOptionCollection:
            """
            Retrieves the child collection at the given name. The name search is case
            insensitive.
            """
            ...

        def CopyTo(self, array: System.Array, index: int) -> None:
            """Copies this collection to an array."""
            ...

        def GetEnumerator(self) -> System.Collections.IEnumerator:
            """Returns an enumerator that can be used to iterate this collection."""
            ...

        def IndexOf(self, value: System.ComponentModel.Design.DesignerOptionService.DesignerOptionCollection) -> int:
            """Returns the numerical index of the given value."""
            ...

        def ShowDialog(self) -> bool:
            """
            Displays a dialog-based user interface that allows the user to
            configure the various options.
            """
            ...

    @property
    def Options(self) -> System.ComponentModel.Design.DesignerOptionService.DesignerOptionCollection:
        """
        Returns the options collection for this service. There is
        always a global options collection that contains child collections.
        """
        ...

    def CreateOptionCollection(self, parent: System.ComponentModel.Design.DesignerOptionService.DesignerOptionCollection, name: str, value: typing.Any) -> System.ComponentModel.Design.DesignerOptionService.DesignerOptionCollection:
        """
        Creates a new DesignerOptionCollection with the given name, and adds it to
        the given parent. The "value" parameter specifies an object whose public
        properties will be used in the Properties collection of the option collection.
        The value parameter can be null if this options collection does not offer
        any properties. Properties will be wrapped in such a way that passing
        anything into the component parameter of the property descriptor will be
        ignored and the value object will be substituted.
        
        This method is protected.
        """
        ...

    def PopulateOptionCollection(self, options: System.ComponentModel.Design.DesignerOptionService.DesignerOptionCollection) -> None:
        """
        This method is called on demand the first time a user asks for child
        options or properties of an options collection.
        
        This method is protected.
        """
        ...

    def ShowDialog(self, options: System.ComponentModel.Design.DesignerOptionService.DesignerOptionCollection, optionObject: typing.Any) -> bool:
        """
        This method must be implemented to show the options dialog UI for the given object.
        
        This method is protected.
        """
        ...


class DesignerVerbCollection(System.Collections.CollectionBase):
    """This class has no documentation."""

    def __getitem__(self, index: int) -> System.ComponentModel.Design.DesignerVerb:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, value: typing.List[System.ComponentModel.Design.DesignerVerb]) -> None:
        ...

    def __setitem__(self, index: int, value: System.ComponentModel.Design.DesignerVerb) -> None:
        ...

    def Add(self, value: System.ComponentModel.Design.DesignerVerb) -> int:
        ...

    @overload
    def AddRange(self, value: typing.List[System.ComponentModel.Design.DesignerVerb]) -> None:
        ...

    @overload
    def AddRange(self, value: System.ComponentModel.Design.DesignerVerbCollection) -> None:
        ...

    def Contains(self, value: System.ComponentModel.Design.DesignerVerb) -> bool:
        ...

    def CopyTo(self, array: typing.List[System.ComponentModel.Design.DesignerVerb], index: int) -> None:
        ...

    def IndexOf(self, value: System.ComponentModel.Design.DesignerVerb) -> int:
        ...

    def Insert(self, index: int, value: System.ComponentModel.Design.DesignerVerb) -> None:
        ...

    def OnValidate(self, value: typing.Any) -> None:
        """This method is protected."""
        ...

    def Remove(self, value: System.ComponentModel.Design.DesignerVerb) -> None:
        ...


class IMenuCommandService(metaclass=abc.ABCMeta):
    """
    Provides an interface for a designer to add menu items to the Visual Studio
    7.0 menu.
    """


class IRootDesigner(System.ComponentModel.Design.IDesigner, metaclass=abc.ABCMeta):
    """
    Defines the root designer. A root designer is the designer that sits
    at the top, or root, of the object hierarchy. The root designer's job
    is to provide the design-time user interface for the design surface.
    It does this through the View property.
    """


class ComponentEventArgs(System.EventArgs):
    """
    Provides data for the System.ComponentModel.Design.IComponentChangeService.ComponentEvent
    event raised for component-level events.
    """

    @property
    def Component(self) -> System.ComponentModel.IComponent:
        """Gets or sets the component associated with the event."""
        ...

    def __init__(self, component: System.ComponentModel.IComponent) -> None:
        """Initializes a new instance of the System.ComponentModel.Design.ComponentEventArgs class."""
        ...


class CheckoutException(System.Runtime.InteropServices.ExternalException):
    """
    The exception thrown when an attempt is made to edit a file that is checked into
    a source control program.
    """

    Canceled: System.ComponentModel.Design.CheckoutException = ...
    """
    Initializes a System.ComponentModel.Design.CheckoutException that specifies that the checkout
    was canceled. This field is read-only.
    """

    @overload
    def __init__(self) -> None:
        """
        Initializes a new instance of the System.ComponentModel.Design.CheckoutException class with
        no associated message or error code.
        """
        ...

    @overload
    def __init__(self, message: str) -> None:
        """
        Initializes a new instance of the System.ComponentModel.Design.CheckoutException
        class with the specified message.
        """
        ...

    @overload
    def __init__(self, message: str, errorCode: int) -> None:
        """
        Initializes a new instance of the System.ComponentModel.Design.CheckoutException
        class with the specified message and error code.
        """
        ...

    @overload
    def __init__(self, message: str, innerException: System.Exception) -> None:
        """
        Initializes a new instance of the Exception class with a specified error message and a
        reference to the inner exception that is the cause of this exception.
        FxCop CA1032: Multiple constructors are required to correctly implement a custom exception.
        """
        ...

    @overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        Need this constructor since Exception implements ISerializable. We don't have any fields,
        so just forward this to base.
        
        This method is protected.
        
        Obsoletions.LegacyFormatterImplMessage
        """
        ...


class ISelectionService(metaclass=abc.ABCMeta):
    """Provides an interface for a designer to select components."""


class IDictionaryService(metaclass=abc.ABCMeta):
    """
    Provides a generic dictionary service that a designer can use
    to store user-defined data on the site.
    """


class _EventContainer(typing.Generic[System_ComponentModel_Design__EventContainer_Callable, System_ComponentModel_Design__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> System_ComponentModel_Design__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: System_ComponentModel_Design__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: System_ComponentModel_Design__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


