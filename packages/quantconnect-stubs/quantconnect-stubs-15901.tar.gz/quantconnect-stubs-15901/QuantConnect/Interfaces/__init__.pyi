from typing import overload
import abc
import typing

import QuantConnect.Api
import QuantConnect.Interfaces
import QuantConnect.Optimizer.Objectives
import QuantConnect.Optimizer.Parameters
import System
import System.Collections.Generic

QuantConnect_Interfaces_IExtendedDictionary_TKey = typing.TypeVar("QuantConnect_Interfaces_IExtendedDictionary_TKey")
QuantConnect_Interfaces_IExtendedDictionary_TValue = typing.TypeVar("QuantConnect_Interfaces_IExtendedDictionary_TValue")
QuantConnect_Interfaces_IBusyCollection_T = typing.TypeVar("QuantConnect_Interfaces_IBusyCollection_T")
QuantConnect_Interfaces__EventContainer_Callable = typing.TypeVar("QuantConnect_Interfaces__EventContainer_Callable")
QuantConnect_Interfaces__EventContainer_ReturnType = typing.TypeVar("QuantConnect_Interfaces__EventContainer_ReturnType")


class IApi(System.IDisposable, metaclass=abc.ABCMeta):
    """API for QuantConnect.com"""

    def AbortOptimization(self, optimizationId: str) -> QuantConnect.Api.RestResponse:
        """
        Abort an optimization
        
        :param optimizationId: Optimization id for the optimization we want to abort
        :returns: RestResponse.
        """
        ...

    def CreateOptimization(self, projectId: int, name: str, target: str, targetTo: str, targetValue: typing.Optional[float], strategy: str, compileId: str, parameters: System.Collections.Generic.HashSet[QuantConnect.Optimizer.Parameters.OptimizationParameter], constraints: System.Collections.Generic.IReadOnlyList[QuantConnect.Optimizer.Objectives.Constraint], estimatedCost: float, nodeType: str, parallelNodes: int) -> QuantConnect.Api.BaseOptimization:
        """
        Create an optimization with the specified parameters via QuantConnect.com API
        
        :param projectId: Project ID of the project the optimization belongs to
        :param name: Name of the optimization
        :param target: Target of the optimization, see examples in PortfolioStatistics
        :param targetTo: Target extremum of the optimization, for example "max" or "min"
        :param targetValue: Optimization target value
        :param strategy: Optimization strategy, GridSearchOptimizationStrategy
        :param compileId: Optimization compile ID
        :param parameters: Optimization parameters
        :param constraints: Optimization constraints
        :param estimatedCost: Estimated cost for optimization
        :param nodeType: Optimization node type
        :param parallelNodes: Number of parallel nodes for optimization
        :returns: BaseOptimization object from the API.
        """
        ...

    def DeleteOptimization(self, optimizationId: str) -> QuantConnect.Api.RestResponse:
        """
        Delete an optimization
        
        :param optimizationId: Optimization id for the optimization we want to delete
        :returns: RestResponse.
        """
        ...

    def EstimateOptimization(self, projectId: int, name: str, target: str, targetTo: str, targetValue: typing.Optional[float], strategy: str, compileId: str, parameters: System.Collections.Generic.HashSet[QuantConnect.Optimizer.Parameters.OptimizationParameter], constraints: System.Collections.Generic.IReadOnlyList[QuantConnect.Optimizer.Objectives.Constraint]) -> QuantConnect.Api.Estimate:
        """
        Estimate optimization with the specified parameters via QuantConnect.com API
        
        :param projectId: Project ID of the project the optimization belongs to
        :param name: Name of the optimization
        :param target: Target of the optimization, see examples in PortfolioStatistics
        :param targetTo: Target extremum of the optimization, for example "max" or "min"
        :param targetValue: Optimization target value
        :param strategy: Optimization strategy, GridSearchOptimizationStrategy
        :param compileId: Optimization compile ID
        :param parameters: Optimization parameters
        :param constraints: Optimization constraints
        :returns: Estimate object from the API.
        """
        ...

    def ListOptimizations(self, projectId: int) -> System.Collections.Generic.List[QuantConnect.Api.BaseOptimization]:
        """
        List all the optimizations for a project
        
        :param projectId: Project id we'd like to get a list of optimizations for
        :returns: A list of BaseOptimization objects, BaseOptimization.
        """
        ...

    def ListOrganizations(self) -> System.Collections.Generic.List[QuantConnect.Api.Organization]:
        """Get a list of organizations tied to this account"""
        ...

    def ReadAccount(self, organizationId: str = None) -> QuantConnect.Api.Account:
        """
        Will read the organization account status
        
        :param organizationId: The target organization id, if null will return default organization
        """
        ...

    def ReadBacktestReport(self, projectId: int, backtestId: str) -> QuantConnect.Api.BacktestReport:
        """
        Read out the report of a backtest in the project id specified.
        
        :param projectId: Project id to read
        :param backtestId: Specific backtest id to read
        :returns: BacktestReport.
        """
        ...

    def ReadDataPrices(self, organizationId: str) -> QuantConnect.Api.DataPricesList:
        """Gets data prices from data/prices"""
        ...

    def ReadOptimization(self, optimizationId: str) -> QuantConnect.Api.Optimization:
        """
        Read an optimization
        
        :param optimizationId: Optimization id for the optimization we want to read
        :returns: Optimization.
        """
        ...

    def ReadOrganization(self, organizationId: str = None) -> QuantConnect.Api.Organization:
        """Fetch organization data from web API"""
        ...

    def UpdateOptimization(self, optimizationId: str, name: str = None) -> QuantConnect.Api.RestResponse:
        """
        Update an optimization
        
        :param optimizationId: Optimization id we want to update
        :param name: Name we'd like to assign to the optimization
        :returns: RestResponse.
        """
        ...


class IDataProvider(metaclass=abc.ABCMeta):
    """
    Fetches a remote file for a security.
    Must save the file to Globals.DataFolder.
    """


class IObjectStore(System.IDisposable, metaclass=abc.ABCMeta):
    """Provides object storage for data persistence."""


class ISubscriptionDataConfigProvider(metaclass=abc.ABCMeta):
    """Reduced interface which provides access to registered SubscriptionDataConfig"""


class ISubscriptionDataConfigService(QuantConnect.Interfaces.ISubscriptionDataConfigProvider, metaclass=abc.ABCMeta):
    """
    This interface exposes methods for creating a list of SubscriptionDataConfig for a given
    configuration
    """


class IAlgorithmSubscriptionManager(QuantConnect.Interfaces.ISubscriptionDataConfigService, metaclass=abc.ABCMeta):
    """AlgorithmSubscriptionManager interface will manage the subscriptions for the SubscriptionManager"""


class ISecurityPrice(metaclass=abc.ABCMeta):
    """
    Reduced interface which allows setting and accessing
    price properties for a Security
    """


class IAccountCurrencyProvider(metaclass=abc.ABCMeta):
    """A reduced interface for an account currency provider"""


class IRegressionAlgorithmDefinition(metaclass=abc.ABCMeta):
    """
    Defines a C# algorithm as a regression algorithm to be run as part of the test suite.
    This interface also allows the algorithm to declare that it has versions in other languages
    that should yield identical results.
    """


class IDataChannelProvider(metaclass=abc.ABCMeta):
    """Specifies data channel settings"""


class IDataCacheProvider(System.IDisposable, metaclass=abc.ABCMeta):
    """Defines a cache for data"""


class IShortableProvider(metaclass=abc.ABCMeta):
    """Defines a short list/easy-to-borrow provider"""


class ITradeBuilder(metaclass=abc.ABCMeta):
    """Generates trades from executions and market price updates"""


class IMapFileProvider(metaclass=abc.ABCMeta):
    """Provides instances of MapFileResolver at run time"""


class IMessagingHandler(System.IDisposable, metaclass=abc.ABCMeta):
    """
    Messaging System Plugin Interface.
    Provides a common messaging pattern between desktop and cloud implementations of QuantConnect.
    """


class IAlgorithmSettings(metaclass=abc.ABCMeta):
    """User settings for the algorithm which can be changed in the IAlgorithm.Initialize method"""


class DataProviderNewDataRequestEventArgs(System.EventArgs):
    """Event arguments for the IDataProvider.NewDataRequest event"""

    @property
    def Path(self) -> str:
        """Path to the fetched data"""
        ...

    @property
    def Succeded(self) -> bool:
        """Whether the data was fetched successfully"""
        ...

    def __init__(self, path: str, succeded: bool) -> None:
        """
        Initializes a new instance of the DataProviderNewDataRequestEventArgs class
        
        :param path: The path to the fetched data
        :param succeded: Whether the data was fetched successfully
        """
        ...


class ISecurityService(metaclass=abc.ABCMeta):
    """This interface exposes methods for creating a new Security"""


class IFactorFileProvider(metaclass=abc.ABCMeta):
    """Provides instances of FactorFile at run time"""


class ObjectStoreErrorRaisedEventArgs(System.EventArgs):
    """Event arguments for the IObjectStore.ErrorRaised event"""

    @property
    def Error(self) -> System.Exception:
        """Gets the Exception that was raised"""
        ...

    def __init__(self, error: System.Exception) -> None:
        """
        Initializes a new instance of the ObjectStoreErrorRaisedEventArgs class
        
        :param error: The error that was raised
        """
        ...


class IDataProviderEvents(metaclass=abc.ABCMeta):
    """Events related to data providers"""


class ITimeKeeper(metaclass=abc.ABCMeta):
    """Interface implemented by TimeKeeper"""


class ISecurityInitializerProvider(metaclass=abc.ABCMeta):
    """Reduced interface which provides an instance which implements ISecurityInitializer"""


class IAlgorithm(QuantConnect.Interfaces.ISecurityInitializerProvider, QuantConnect.Interfaces.IAccountCurrencyProvider, metaclass=abc.ABCMeta):
    """
    Interface for QuantConnect algorithm implementations. All algorithms must implement these
    basic members to allow interaction with the Lean Backtesting Engine.
    """


class IExtendedDictionary(typing.Generic[QuantConnect_Interfaces_IExtendedDictionary_TKey, QuantConnect_Interfaces_IExtendedDictionary_TValue], metaclass=abc.ABCMeta):
    """Represents a generic collection of key/value pairs that implements python dictionary methods."""


class IHistoryProvider(QuantConnect.Interfaces.IDataProviderEvents, metaclass=abc.ABCMeta):
    """Provides historical data to an algorithm at runtime"""


class IBrokerageFactory(System.IDisposable, metaclass=abc.ABCMeta):
    """Defines factory types for brokerages. Every IBrokerage is expected to also implement an IBrokerageFactory."""


class IOptionPrice(QuantConnect.Interfaces.ISecurityPrice, metaclass=abc.ABCMeta):
    """
    Reduced interface for accessing Option
    specific price properties and methods
    """


class IDataQueueHandler(System.IDisposable, metaclass=abc.ABCMeta):
    """Task requestor interface with cloud system"""


class IPriceProvider(metaclass=abc.ABCMeta):
    """Provides access to price data for a given asset"""


class IJobQueueHandler(metaclass=abc.ABCMeta):
    """Task requestor interface with cloud system"""


class IDataMonitor(System.IDisposable, metaclass=abc.ABCMeta):
    """Monitors data requests and reports on missing data"""


class IRegressionResearchDefinition(metaclass=abc.ABCMeta):
    """Defines interface for research notebooks to be run as part of the research test suite."""


class IFutureChainProvider(metaclass=abc.ABCMeta):
    """Provides the full future chain for a given underlying."""


class IOptionChainProvider(metaclass=abc.ABCMeta):
    """Provides the full option chain for a given underlying."""


class IDownloadProvider(metaclass=abc.ABCMeta):
    """Wrapper on the API for downloading data for an algorithm."""


class IPrimaryExchangeProvider(metaclass=abc.ABCMeta):
    """Primary Exchange Provider interface"""


class IOrderProperties(metaclass=abc.ABCMeta):
    """Contains additional properties and settings for an order"""


class MessagingHandlerInitializeParameters(System.Object):
    """Parameters required to initialize a IMessagingHandler instance"""

    @property
    def Api(self) -> QuantConnect.Interfaces.IApi:
        """The api instance to use"""
        ...

    def __init__(self, api: QuantConnect.Interfaces.IApi) -> None:
        """
        Creates a new instance
        
        :param api: The api instance to use
        """
        ...


class IStreamReader(System.IDisposable, metaclass=abc.ABCMeta):
    """Defines a transport mechanism for data from its source into various reader methods"""


class IBrokerageCashSynchronizer(metaclass=abc.ABCMeta):
    """Defines live brokerage cash synchronization operations."""


class IBrokerage(QuantConnect.Interfaces.IBrokerageCashSynchronizer, System.IDisposable, metaclass=abc.ABCMeta):
    """
    Brokerage interface that defines the operations all brokerages must implement. The IBrokerage implementation
    must have a matching IBrokerageFactory implementation.
    """


class IDataPermissionManager(metaclass=abc.ABCMeta):
    """Entity in charge of handling data permissions"""


class ISignalExportTarget(System.IDisposable, metaclass=abc.ABCMeta):
    """Interface to send positions holdings to different 3rd party API's"""


class ITimeInForceHandler(metaclass=abc.ABCMeta):
    """Handles the time in force for an order"""


class IBusyCollection(typing.Generic[QuantConnect_Interfaces_IBusyCollection_T], System.IDisposable, metaclass=abc.ABCMeta):
    """Interface used to handle items being processed and communicate busy state"""


class IDataQueueUniverseProvider(metaclass=abc.ABCMeta):
    """
    This interface allows interested parties to lookup or enumerate the available symbols. Data source exposes it if this feature is available.
    Availability of a symbol doesn't imply that it is possible to trade it. This is a data source specific interface, not broker specific.
    """


class _EventContainer(typing.Generic[QuantConnect_Interfaces__EventContainer_Callable, QuantConnect_Interfaces__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> QuantConnect_Interfaces__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: QuantConnect_Interfaces__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: QuantConnect_Interfaces__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


