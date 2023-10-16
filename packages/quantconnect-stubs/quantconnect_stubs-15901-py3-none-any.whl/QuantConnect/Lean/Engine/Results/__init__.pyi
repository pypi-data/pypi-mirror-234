from typing import overload
import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Brokerages
import QuantConnect.Data.Market
import QuantConnect.Data.UniverseSelection
import QuantConnect.Interfaces
import QuantConnect.Lean.Engine.Results
import QuantConnect.Lean.Engine.TransactionHandlers
import QuantConnect.Logging
import QuantConnect.Orders
import QuantConnect.Orders.Serialization
import QuantConnect.Packets
import QuantConnect.Securities
import QuantConnect.Statistics
import System
import System.Collections.Concurrent
import System.Collections.Generic
import System.Threading


class BaseResultsHandler(System.Object, metaclass=abc.ABCMeta):
    """Provides base functionality to the implementations of IResultHandler"""

    StrategyEquityKey: str = "Strategy Equity"
    """This field is protected."""

    EquityKey: str = "Equity"
    """This field is protected."""

    DailyPerformanceKey: str = "Daily Performance"
    """This field is protected."""

    BenchmarkKey: str = "Benchmark"
    """This field is protected."""

    DrawdownKey: str = "Drawdown"
    """This field is protected."""

    PortfolioTurnoverKey: str = "Portfolio Turnover"
    """This field is protected."""

    @property
    def MainUpdateInterval(self) -> datetime.timedelta:
        """
        The main loop update interval
        
        This property is protected.
        """
        ...

    @property
    def ChartUpdateInterval(self) -> datetime.timedelta:
        """
        The chart update interval
        
        This field is protected.
        """
        ...

    @property
    def LastDeltaOrderPosition(self) -> int:
        """
        The last position consumed from the ITransactionHandler.OrderEvents by GetDeltaOrders
        
        This field is protected.
        """
        ...

    @property
    def LastDeltaOrderEventsPosition(self) -> int:
        """
        The last position consumed from the ITransactionHandler.OrderEvents while determining delta order events
        
        This field is protected.
        """
        ...

    @property
    def CurrentAlgorithmEquity(self) -> QuantConnect.Data.Market.Bar:
        """
        The current aggregated equity bar for sampling.
        It will be aggregated with values from the GetPortfolioValue
        
        This property is protected.
        """
        ...

    @property
    def IsActive(self) -> bool:
        """Boolean flag indicating the thread is still active."""
        ...

    @property
    def Messages(self) -> System.Collections.Concurrent.ConcurrentQueue[QuantConnect.Packets.Packet]:
        """Live packet messaging queue. Queue the messages here and send when the result queue is ready."""
        ...

    @property
    def Charts(self) -> System.Collections.Concurrent.ConcurrentDictionary[str, QuantConnect.Chart]:
        """Storage for the price and equity charts of the live results."""
        ...

    @property
    def ExitTriggered(self) -> bool:
        """
        True if the exit has been triggered
        
        This field is protected.
        """
        ...

    @property
    def ExitEvent(self) -> System.Threading.ManualResetEvent:
        """
        Event set when exit is triggered
        
        This property is protected.
        """
        ...

    @property
    def LogStore(self) -> System.Collections.Generic.List[QuantConnect.Logging.LogEntry]:
        """
        The log store instance
        
        This property is protected.
        """
        ...

    @property
    def AlgorithmPerformanceCharts(self) -> System.Collections.Generic.List[str]:
        """
        Algorithms performance related chart names
        
        This property is protected.
        """
        ...

    @property
    def ChartLock(self) -> System.Object:
        """
        Lock to be used when accessing the chart collection
        
        This property is protected.
        """
        ...

    @property
    def ProjectId(self) -> int:
        """
        The algorithm project id
        
        This property is protected.
        """
        ...

    @property
    def RamAllocation(self) -> str:
        """
        The maximum amount of RAM (in MB) this algorithm is allowed to utilize
        
        This property is protected.
        """
        ...

    @property
    def CompileId(self) -> str:
        """
        The algorithm unique compilation id
        
        This property is protected.
        """
        ...

    @property
    def AlgorithmId(self) -> str:
        """
        The algorithm job id.
        This is the deploy id for live, backtesting id for backtesting
        
        This property is protected.
        """
        ...

    @property
    def StartTime(self) -> datetime.datetime:
        """
        The result handler start time
        
        This property is protected.
        """
        ...

    @property
    def RuntimeStatistics(self) -> System.Collections.Generic.Dictionary[str, str]:
        """
        Customizable dynamic statistics IAlgorithm.RuntimeStatistics
        
        This property is protected.
        """
        ...

    @property
    def State(self) -> System.Collections.Generic.Dictionary[str, str]:
        """
        State of the algorithm
        
        This property is protected.
        """
        ...

    @property
    def MessagingHandler(self) -> QuantConnect.Interfaces.IMessagingHandler:
        """
        The handler responsible for communicating messages to listeners
        
        This field is protected.
        """
        ...

    @property
    def TransactionHandler(self) -> QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler:
        """
        The transaction handler used to get the algorithms Orders information
        
        This field is protected.
        """
        ...

    @property
    def StartingPortfolioValue(self) -> float:
        """
        The algorithms starting portfolio value.
        Used to calculate the portfolio return
        
        This property is protected.
        """
        ...

    @property
    def Algorithm(self) -> QuantConnect.Interfaces.IAlgorithm:
        """
        The algorithm instance
        
        This property is protected.
        """
        ...

    @property
    def AlgorithmCurrencySymbol(self) -> str:
        """
        Algorithm currency symbol, used in charting
        
        This property is protected.
        """
        ...

    @property
    def DailyPortfolioValue(self) -> float:
        """
        Closing portfolio value. Used to calculate daily performance.
        
        This field is protected.
        """
        ...

    @property
    def CumulativeMaxPortfolioValue(self) -> float:
        """
        Cumulative max portfolio value. Used to calculate drawdown underwater.
        
        This field is protected.
        """
        ...

    @property
    def ResamplePeriod(self) -> datetime.timedelta:
        """
        Sampling period for timespans between resamples of the charting equity.
        
        This property is protected.
        """
        ...

    @property
    def NotificationPeriod(self) -> datetime.timedelta:
        """
        How frequently the backtests push messages to the browser.
        
        This property is protected.
        """
        ...

    @property
    def ResultsDestinationFolder(self) -> str:
        """
        Directory location to store results
        
        This field is protected.
        """
        ...

    @property
    def OrderEventJsonConverter(self) -> QuantConnect.Orders.Serialization.OrderEventJsonConverter:
        """
        The order event json converter instance to use
        
        This property is protected.
        """
        ...

    def __init__(self) -> None:
        """
        Creates a new instance
        
        This method is protected.
        """
        ...

    def AddToLogStore(self, message: str) -> None:
        """
        Save an algorithm message to the log store. Uses a different timestamped method of adding messaging to interweve debug and logging messages.
        
        This method is protected.
        
        :param message: String message to store
        """
        ...

    def Exit(self) -> None:
        """Terminate the result thread and apply any required exit procedures like sending final results"""
        ...

    @overload
    def GenerateStatisticsResults(self, charts: System.Collections.Generic.Dictionary[str, QuantConnect.Chart], profitLoss: System.Collections.Generic.SortedDictionary[datetime.datetime, float] = None, estimatedStrategyCapacity: QuantConnect.CapacityEstimate = None) -> QuantConnect.Statistics.StatisticsResults:
        """
        Will generate the statistics results and update the provided runtime statistics
        
        This method is protected.
        """
        ...

    @overload
    def GenerateStatisticsResults(self, estimatedStrategyCapacity: QuantConnect.CapacityEstimate = None) -> QuantConnect.Statistics.StatisticsResults:
        """
        Calculates and gets the current statistics for the algorithm.
        It will use the current Charts and profit loss information calculated from the current transaction record
        to generate the results.
        
        This method is protected.
        
        :returns: The current statistics.
        """
        ...

    def GetAlgorithmRuntimeStatistics(self, summary: System.Collections.Generic.Dictionary[str, str], capacityEstimate: QuantConnect.CapacityEstimate = None) -> System.Collections.Generic.SortedDictionary[str, str]:
        """
        Gets the algorithm runtime statistics
        
        This method is protected.
        """
        ...

    def GetAlgorithmState(self, endTime: typing.Optional[datetime.datetime] = None) -> System.Collections.Generic.Dictionary[str, str]:
        """
        Gets the algorithm state data
        
        This method is protected.
        """
        ...

    def GetBenchmarkValue(self, time: typing.Union[datetime.datetime, datetime.date]) -> float:
        """
        Gets the current benchmark value
        
        This method is protected.
        
        :param time: Time to resolve benchmark value at
        """
        ...

    def GetDeltaOrders(self, orderEventsStartPosition: int, shouldStop: typing.Callable[[int], bool]) -> System.Collections.Generic.Dictionary[int, QuantConnect.Orders.Order]:
        """
        Gets the orders generated starting from the provided ITransactionHandler.OrderEvents position
        
        This method is protected.
        
        :returns: The delta orders.
        """
        ...

    def GetNetReturn(self) -> float:
        """
        Gets the algorithm net return
        
        This method is protected.
        """
        ...

    def GetPortfolioValue(self) -> float:
        """
        Gets the current portfolio value
        
        This method is protected.
        """
        ...

    def GetResultsPath(self, filename: str) -> str:
        """
        Gets the full path for a results file
        
        This method is protected.
        
        :param filename: The filename to add to the path
        :returns: The full path, including the filename.
        """
        ...

    def GetServerStatistics(self, utcNow: typing.Union[datetime.datetime, datetime.date]) -> System.Collections.Generic.Dictionary[str, str]:
        """
        Gets the current Server statistics
        
        This method is protected.
        """
        ...

    def Initialize(self, job: QuantConnect.Packets.AlgorithmNodePacket, messagingHandler: QuantConnect.Interfaces.IMessagingHandler, api: QuantConnect.Interfaces.IApi, transactionHandler: QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler) -> None:
        """
        Initialize the result handler with this result packet.
        
        :param job: Algorithm job packet for this result handler
        :param messagingHandler: The handler responsible for communicating messages to listeners
        :param api: The api instance used for handling logs
        :param transactionHandler: The transaction handler used to get the algorithms Order information
        """
        ...

    def OnSecuritiesChanged(self, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """Event fired each time that we add/remove securities from the data feed"""
        ...

    def OrderEvent(self, newEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        New order event for the algorithm
        
        :param newEvent: New event details
        """
        ...

    def ProcessAlgorithmLogs(self, messageQueueLimit: typing.Optional[int] = None) -> None:
        """
        Processes algorithm logs.
        Logs of the same type are batched together one per line and are sent out
        
        This method is protected.
        """
        ...

    def PurgeQueue(self) -> None:
        """
        Purge/clear any outstanding messages in message queue.
        
        This method is protected.
        """
        ...

    def Run(self) -> None:
        """
        Result handler update method
        
        This method is protected.
        """
        ...

    @overload
    def Sample(self, time: typing.Union[datetime.datetime, datetime.date]) -> None:
        """
        Samples portfolio equity, benchmark, and daily performance
        Called by scheduled event every night at midnight algorithm time
        
        :param time: Current UTC time in the AlgorithmManager loop
        """
        ...

    @overload
    def Sample(self, chartName: str, seriesName: str, seriesIndex: int, seriesType: QuantConnect.SeriesType, value: QuantConnect.ISeriesPoint, unit: str = "$") -> None:
        """
        Add a sample to the chart specified by the chartName, and seriesName.
        
        This method is protected.
        
        :param chartName: String chart name to place the sample.
        :param seriesName: Series name for the chart.
        :param seriesIndex: Series chart index - which chart should this series belong
        :param seriesType: Series type for the chart.
        :param value: Value for the chart sample.
        :param unit: Unit for the chart axis
        """
        ...

    def SampleBenchmark(self, time: typing.Union[datetime.datetime, datetime.date], value: float) -> None:
        """
        Sample the current benchmark performance directly with a time-value pair.
        
        This method is protected.
        
        :param time: Time of the sample.
        :param value: Current benchmark value.
        """
        ...

    def SampleCapacity(self, time: typing.Union[datetime.datetime, datetime.date]) -> None:
        """
        Sample estimated strategy capacity
        
        This method is protected.
        
        :param time: Time of the sample
        """
        ...

    def SampleDrawdown(self, time: typing.Union[datetime.datetime, datetime.date], currentPortfolioValue: float) -> None:
        """
        Sample drawdown of equity of the strategy
        
        This method is protected.
        
        :param time: Time of the sample
        :param currentPortfolioValue: Current equity value
        """
        ...

    def SampleEquity(self, time: typing.Union[datetime.datetime, datetime.date]) -> None:
        """
        Sample the current equity of the strategy directly with time and using
        the current algorithm equity value in CurrentAlgorithmEquity
        
        This method is protected.
        
        :param time: Equity candlestick end time
        """
        ...

    def SampleExposure(self, time: typing.Union[datetime.datetime, datetime.date], currentPortfolioValue: float) -> None:
        """
        Sample portfolio exposure long/short ratios by security type
        
        This method is protected.
        
        :param time: Time of the sample
        :param currentPortfolioValue: Current value of the portfolio
        """
        ...

    def SamplePerformance(self, time: typing.Union[datetime.datetime, datetime.date], value: float) -> None:
        """
        Sample the current daily performance directly with a time-value pair.
        
        This method is protected.
        
        :param time: Time of the sample.
        :param value: Current daily performance value.
        """
        ...

    def SamplePortfolioTurnover(self, time: typing.Union[datetime.datetime, datetime.date], currentPortfolioValue: float) -> None:
        """
        Sample portfolio turn over of the strategy
        
        This method is protected.
        
        :param time: Time of the sample
        :param currentPortfolioValue: Current equity value
        """
        ...

    def SampleSalesVolume(self, time: typing.Union[datetime.datetime, datetime.date]) -> None:
        """
        Sample assets sales volume
        
        This method is protected.
        
        :param time: Time of the sample
        """
        ...

    def SaveLogs(self, id: str, logs: System.Collections.Generic.List[QuantConnect.Logging.LogEntry]) -> str:
        """
        Returns the location of the logs
        
        :param id: Id that will be incorporated into the algorithm log name
        :param logs: The logs to save
        :returns: The path to the logs.
        """
        ...

    def SaveResults(self, name: str, result: QuantConnect.Result) -> None:
        """
        Save the results to disk
        
        :param name: The name of the results
        :param result: The results to save
        """
        ...

    def SetAlgorithmState(self, error: str, stack: str) -> None:
        """
        Sets the algorithm state data
        
        This method is protected.
        """
        ...

    def StopUpdateRunner(self) -> None:
        """
        Stops the update runner task
        
        This method is protected.
        """
        ...

    def StoreInsights(self) -> None:
        """
        Save insight results to persistent storage
        
        This method is protected.
        """
        ...

    def StoreOrderEvents(self, utcTime: typing.Union[datetime.datetime, datetime.date], orderEvents: System.Collections.Generic.List[QuantConnect.Orders.OrderEvent]) -> None:
        """
        Stores the order events
        
        This method is protected.
        
        :param utcTime: The utc date associated with these order events
        :param orderEvents: The order events to store
        """
        ...

    def StoreResult(self, packet: QuantConnect.Packets.Packet) -> None:
        """
        Save the snapshot of the total results to storage.
        
        This method is protected.
        
        :param packet: Packet to store.
        """
        ...

    def SummaryStatistic(self, name: str, value: str) -> None:
        """
        Sets or updates a custom summary statistic
        
        This method is protected.
        
        :param name: The statistic name
        :param value: The statistic value
        """
        ...

    def UpdateAlgorithmEquity(self) -> None:
        """
        Updates the current equity bar with the current equity value from GetPortfolioValue
        
        This method is protected.
        """
        ...


class IResultHandler(QuantConnect.Statistics.IStatisticsService, metaclass=abc.ABCMeta):
    """
    Handle the results of the backtest: where should we send the profit, portfolio updates:
    Backtester or the Live trading platform:
    """


class BacktestingResultHandler(QuantConnect.Lean.Engine.Results.BaseResultsHandler, QuantConnect.Lean.Engine.Results.IResultHandler):
    """Backtesting result handler passes messages back from the Lean to the User."""

    @property
    def FinalStatistics(self) -> System.Collections.Generic.Dictionary[str, str]:
        """A dictionary containing summary statistics"""
        ...

    def __init__(self) -> None:
        """Creates a new instance"""
        ...

    def AddToLogStore(self, message: str) -> None:
        """
        Add message to LogStore
        
        This method is protected.
        
        :param message: Message to add
        """
        ...

    def BrokerageMessage(self, brokerageMessageEvent: QuantConnect.Brokerages.BrokerageMessageEvent) -> None:
        """
        Process brokerage message events
        
        :param brokerageMessageEvent: The brokerage message event
        """
        ...

    def ConfigureConsoleTextWriter(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        """
        Configures the Console.Out and Console.ErrorTextWriter
        instances. By default, we forward Console.WriteLine(string) to IAlgorithm.Debug.
        This is perfect for running in the cloud, but since they're processed asynchronously, the ordering of these
        messages with respect to Log messages is broken. This can lead to differences in regression
        test logs based solely on the ordering of messages. To disable this forwarding, set "forward-console-messages"
        to false in the configuration.
        
        This method is protected.
        """
        ...

    def DebugMessage(self, message: str) -> None:
        """
        Send a debug message back to the browser console.
        
        :param message: Message we'd like shown in console.
        """
        ...

    def ErrorMessage(self, message: str, stacktrace: str = ...) -> None:
        """
        Send an error message back to the browser highlighted in red with a stacktrace.
        
        :param message: Error message we'd like shown in console.
        :param stacktrace: Stacktrace information string
        """
        ...

    def Exit(self) -> None:
        """Terminate the result thread and apply any required exit procedures like sending final results."""
        ...

    def Initialize(self, job: QuantConnect.Packets.AlgorithmNodePacket, messagingHandler: QuantConnect.Interfaces.IMessagingHandler, api: QuantConnect.Interfaces.IApi, transactionHandler: QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler) -> None:
        """
        Initialize the result handler with this result packet.
        
        :param job: Algorithm job packet for this result handler
        :param messagingHandler: The handler responsible for communicating messages to listeners
        :param api: The api instance used for handling logs
        :param transactionHandler: The transaction handler used to get the algorithms Order information
        """
        ...

    def LogMessage(self, message: str) -> None:
        """
        Send a logging message to the log list for storage.
        
        :param message: Message we'd in the log.
        """
        ...

    def OrderEvent(self, newEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Handle order event
        
        :param newEvent: Event to process
        """
        ...

    def ProcessSynchronousEvents(self, forceProcess: bool = False) -> None:
        """
        Process the synchronous result events, sampling and message reading.
        This method is triggered from the algorithm manager thread.
        """
        ...

    def Run(self) -> None:
        """
        The main processing method steps through the messaging queue and processes the messages one by one.
        
        This method is protected.
        """
        ...

    def RuntimeError(self, message: str, stacktrace: str = ...) -> None:
        """
        Send a runtime error message back to the browser highlighted with in red
        
        :param message: Error message.
        :param stacktrace: Stacktrace information string
        """
        ...

    def RuntimeStatistic(self, key: str, value: str) -> None:
        """
        Set the current runtime statistics of the algorithm.
        These are banner/title statistics which show at the top of the live trading results.
        
        :param key: Runtime headline statistic name
        :param value: Runtime headline statistic value
        """
        ...

    def Sample(self, chartName: str, seriesName: str, seriesIndex: int, seriesType: QuantConnect.SeriesType, value: QuantConnect.ISeriesPoint, unit: str = "$") -> None:
        """
        Add a sample to the chart specified by the chartName, and seriesName.
        
        This method is protected.
        
        :param chartName: String chart name to place the sample.
        :param seriesName: Series name for the chart.
        :param seriesIndex: Type of chart we should create if it doesn't already exist.
        :param seriesType: Series type for the chart.
        :param value: Value for the chart sample.
        :param unit: Unit of the sample
        """
        ...

    def SampleCapacity(self, time: typing.Union[datetime.datetime, datetime.date]) -> None:
        """
        Sample estimated strategy capacity
        
        This method is protected.
        
        :param time: Time of the sample
        """
        ...

    def SampleRange(self, updates: System.Collections.Generic.List[QuantConnect.Chart]) -> None:
        """
        Add a range of samples from the users algorithms to the end of our current list.
        
        This method is protected.
        
        :param updates: Chart updates since the last request.
        """
        ...

    def SecurityType(self, types: System.Collections.Generic.List[QuantConnect.SecurityType]) -> None:
        """Send list of security asset types the algorithm uses to browser."""
        ...

    def SendFinalResult(self) -> None:
        """
        Send a final analysis result back to the IDE.
        
        This method is protected.
        """
        ...

    def SendStatusUpdate(self, status: QuantConnect.AlgorithmStatus, message: str = ...) -> None:
        """
        Send an algorithm status update to the browser.
        
        :param status: Status enum value.
        :param message: Additional optional status message.
        """
        ...

    def SetAlgorithm(self, algorithm: QuantConnect.Interfaces.IAlgorithm, startingPortfolioValue: float) -> None:
        """
        Set the Algorithm instance for ths result.
        
        :param algorithm: Algorithm we're working on.
        :param startingPortfolioValue: Algorithm starting capital for statistics calculations
        """
        ...

    def SetSummaryStatistic(self, name: str, value: str) -> None:
        """
        Sets or updates a custom summary statistic
        
        :param name: The statistic name
        :param value: The statistic value
        """
        ...

    def SplitPackets(self, deltaCharts: System.Collections.Generic.Dictionary[str, QuantConnect.Chart], deltaOrders: System.Collections.Generic.Dictionary[int, QuantConnect.Orders.Order], runtimeStatistics: System.Collections.Generic.SortedDictionary[str, str], progress: float, serverStatistics: System.Collections.Generic.Dictionary[str, str]) -> System.Collections.Generic.IEnumerable[QuantConnect.Packets.BacktestResultPacket]:
        """Run over all the data and break it into smaller packets to ensure they all arrive at the terminal"""
        ...

    def StatisticsResults(self) -> QuantConnect.Statistics.StatisticsResults:
        """
        Calculates and gets the current statistics for the algorithm
        
        :returns: The current statistics.
        """
        ...

    def StoreResult(self, packet: QuantConnect.Packets.Packet) -> None:
        """
        Save the snapshot of the total results to storage.
        
        This method is protected.
        
        :param packet: Packet to store.
        """
        ...

    def SystemDebugMessage(self, message: str) -> None:
        """
        Send a system debug message back to the browser console.
        
        :param message: Message we'd like shown in console.
        """
        ...


class BacktestProgressMonitor(System.Object):
    """Monitors and reports the progress of a backtest"""

    @property
    def TotalDays(self) -> int:
        """Gets the total days the algorithm will run"""
        ...

    @property
    def ProcessedDays(self) -> int:
        """Gets the current days the algorithm has been running for"""
        ...

    @property
    def Progress(self) -> float:
        """Gets the current progress of the backtest"""
        ...

    def __init__(self, timeKeeper: QuantConnect.Interfaces.ITimeKeeper, endUtcTime: typing.Union[datetime.datetime, datetime.date]) -> None:
        """
        Creates a new instance
        
        :param timeKeeper: The time keeper to use
        :param endUtcTime: The end UTC time
        """
        ...

    def InvalidateProcessedDays(self) -> None:
        """Invalidates the processed days count value so it gets recalculated next time it is needed"""
        ...


class RegressionResultHandler(QuantConnect.Lean.Engine.Results.BacktestingResultHandler):
    """
    Provides a wrapper over the BacktestingResultHandler that logs all order events
    to a separate file
    """

    @property
    def LogFilePath(self) -> str:
        """Gets the path used for logging all portfolio changing events, such as orders, TPV, daily holdings values"""
        ...

    @property
    def HasRuntimeError(self) -> bool:
        """True if there was a runtime error running the algorithm"""
        ...

    def __init__(self) -> None:
        """Initializes a new instance of the RegressionResultHandler class"""
        ...

    def AddToLogStore(self, message: str) -> None:
        """
        Save an algorithm message to the log store. Uses a different timestamped method of adding messaging to interweve debug and logging messages.
        
        This method is protected.
        
        :param message: String message to store
        """
        ...

    def ConfigureConsoleTextWriter(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        """
        We want to make algorithm messages end up in both the standard regression log file {algorithm}.{language}.log
        as well as the details log {algorithm}.{language}.details.log. The details log is focused on providing a log
        dedicated solely to the algorithm's behavior, void of all QuantConnect.Logging.Log messages
        
        This method is protected.
        """
        ...

    def DebugMessage(self, message: str) -> None:
        """
        Send a debug message back to the browser console.
        
        :param message: Message we'd like shown in console.
        """
        ...

    def ErrorMessage(self, message: str, stacktrace: str = ...) -> None:
        """
        Send an error message back to the browser highlighted in red with a stacktrace.
        
        :param message: Error message we'd like shown in console.
        :param stacktrace: Stacktrace information string
        """
        ...

    def Exit(self) -> None:
        """
        Terminate the result thread and apply any required exit procedures.
        Save orders log files to disk.
        """
        ...

    def LogMessage(self, message: str) -> None:
        """
        Send a logging message to the log list for storage.
        
        :param message: Message we'd in the log.
        """
        ...

    def OnSecuritiesChanged(self, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """Event fired each time that we add/remove securities from the data feed"""
        ...

    def OrderEvent(self, newEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        Log the order and order event to the dedicated log file for this regression algorithm
        
        :param newEvent: New order event details
        """
        ...

    def ProcessSynchronousEvents(self, forceProcess: bool = False) -> None:
        """
        Runs at the end of each time loop. When HighFidelityLogging is enabled, we'll
        log each piece of data to allow for faster determination of regression causes
        """
        ...

    def RuntimeError(self, message: str, stacktrace: str = ...) -> None:
        """
        Send a runtime error message back to the browser highlighted with in red
        
        :param message: Error message.
        :param stacktrace: Stacktrace information string
        """
        ...

    def RuntimeStatistic(self, key: str, value: str) -> None:
        """
        Set the current runtime statistics of the algorithm.
        These are banner/title statistics which show at the top of the live trading results.
        
        :param key: Runtime headline statistic name
        :param value: Runtime headline statistic value
        """
        ...

    def SamplePerformance(self, time: typing.Union[datetime.datetime, datetime.date], value: float) -> None:
        """
        Runs on date changes, use this to log TPV and holdings values each day
        
        This method is protected.
        """
        ...

    def SaveResults(self, name: str, result: QuantConnect.Result) -> None:
        """Save the results to disk"""
        ...

    def SecurityType(self, types: System.Collections.Generic.List[QuantConnect.SecurityType]) -> None:
        """Send list of security asset types the algortihm uses to browser."""
        ...

    def SetAlgorithm(self, algorithm: QuantConnect.Interfaces.IAlgorithm, startingPortfolioValue: float) -> None:
        """Initializes the stream writer using the algorithm's id (name) in the file path"""
        ...

    def SystemDebugMessage(self, message: str) -> None:
        """
        Send a system debug message back to the browser console.
        
        :param message: Message we'd like shown in console.
        """
        ...


class LiveTradingResultHandler(QuantConnect.Lean.Engine.Results.BaseResultsHandler, QuantConnect.Lean.Engine.Results.IResultHandler):
    """Live trading result handler implementation passes the messages to the QC live trading interface."""

    def __init__(self) -> None:
        """Creates a new instance"""
        ...

    def AddToLogStore(self, message: str) -> None:
        """
        Save an algorithm message to the log store. Uses a different timestamped method of adding messaging to interweve debug and logging messages.
        
        This method is protected.
        
        :param message: String message to send to browser.
        """
        ...

    def BrokerageMessage(self, brokerageMessageEvent: QuantConnect.Brokerages.BrokerageMessageEvent) -> None:
        """
        Process brokerage message events
        
        :param brokerageMessageEvent: The brokerage message event
        """
        ...

    def CreateSafeChartName(self, chartName: str) -> str:
        """
        Escape the chartname so that it can be saved to a file system
        
        This method is protected.
        
        :param chartName: The name of a chart
        :returns: The name of the chart will all escape all characters except RFC 2396 unreserved characters.
        """
        ...

    def DebugMessage(self, message: str) -> None:
        """
        Send a live trading debug message to the live console.
        
        :param message: Message we'd like shown in console.
        """
        ...

    def ErrorMessage(self, message: str, stacktrace: str = ...) -> None:
        """
        Send an error message back to the browser console and highlight it read.
        
        :param message: Message we'd like shown in console.
        :param stacktrace: Stacktrace to show in the console.
        """
        ...

    def Exit(self) -> None:
        """Terminate the result thread and apply any required exit procedures like sending final results"""
        ...

    def GetBenchmarkValue(self, time: typing.Union[datetime.datetime, datetime.date]) -> float:
        """
        Gets the current benchmark value
        
        This method is protected.
        
        :param time: Time to resolve benchmark value at
        """
        ...

    @staticmethod
    def GetHoldings(securities: System.Collections.Generic.IEnumerable[QuantConnect.Securities.Security], subscriptionDataConfigService: QuantConnect.Interfaces.ISubscriptionDataConfigService, onlyInvested: bool = False) -> System.Collections.Generic.Dictionary[str, QuantConnect.Holding]:
        """Helper method to fetch the algorithm holdings"""
        ...

    def GetPortfolioValue(self) -> float:
        """
        Gets the current portfolio value
        
        This method is protected.
        """
        ...

    def Initialize(self, job: QuantConnect.Packets.AlgorithmNodePacket, messagingHandler: QuantConnect.Interfaces.IMessagingHandler, api: QuantConnect.Interfaces.IApi, transactionHandler: QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler) -> None:
        """
        Initialize the result handler with this result packet.
        
        :param job: Algorithm job packet for this result handler
        :param messagingHandler: The handler responsible for communicating messages to listeners
        :param api: The api instance used for handling logs
        :param transactionHandler: The transaction handler used to get the algorithms Orders information
        """
        ...

    def LogMessage(self, message: str) -> None:
        """
        Log string messages and send them to the console.
        
        :param message: String message wed like logged.
        """
        ...

    def OnSecuritiesChanged(self, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """
        Event fired each time that we add/remove securities from the data feed.
        On Security change we re determine when should we sample charts, if the user added Crypto, Forex or an extended market hours subscription
        we will always sample charts. Else, we will keep the exchange per market to query later on demand
        """
        ...

    def OrderEvent(self, newEvent: QuantConnect.Orders.OrderEvent) -> None:
        """
        New order event for the algorithm
        
        :param newEvent: New event details
        """
        ...

    def ProcessSynchronousEvents(self, forceProcess: bool = False) -> None:
        """
        Process the synchronous result events, sampling and message reading.
        This method is triggered from the algorithm manager thread.
        """
        ...

    def Run(self) -> None:
        """
        Live trading result handler thread.
        
        This method is protected.
        """
        ...

    def RuntimeError(self, message: str, stacktrace: str = ...) -> None:
        """
        Send a runtime error back to the users browser and highlight it red.
        
        :param message: Runtime error message
        :param stacktrace: Associated error stack trace.
        """
        ...

    def RuntimeStatistic(self, key: str, value: str) -> None:
        """
        Set a dynamic runtime statistic to show in the (live) algorithm header
        
        :param key: Runtime headline statistic name
        :param value: Runtime headline statistic value
        """
        ...

    @overload
    def Sample(self, chartName: str, seriesName: str, seriesIndex: int, seriesType: QuantConnect.SeriesType, value: QuantConnect.ISeriesPoint, unit: str = "$") -> None:
        """
        Add a sample to the chart specified by the chartName, and seriesName.
        
        This method is protected.
        
        :param chartName: String chart name to place the sample.
        :param seriesName: Series name for the chart.
        :param seriesIndex: Series chart index - which chart should this series belong
        :param seriesType: Series type for the chart.
        :param value: Value for the chart sample.
        :param unit: Unit for the chart axis
        """
        ...

    @overload
    def Sample(self, time: typing.Union[datetime.datetime, datetime.date]) -> None:
        """
        Samples portfolio equity, benchmark, and daily performance
        
        :param time: Current UTC time in the AlgorithmManager loop
        """
        ...

    def SampleRange(self, updates: System.Collections.Generic.List[QuantConnect.Chart]) -> None:
        """
        Add a range of samples from the users algorithms to the end of our current list.
        
        This method is protected.
        
        :param updates: Chart updates since the last request.
        """
        ...

    def SaveLogs(self, id: str, logs: System.Collections.Generic.List[QuantConnect.Logging.LogEntry]) -> str:
        """
        Process the log entries and save it to permanent storage
        
        :param id: Id that will be incorporated into the algorithm log name
        :param logs: Log list
        :returns: Returns the location of the logs.
        """
        ...

    def SecurityType(self, types: System.Collections.Generic.List[QuantConnect.SecurityType]) -> None:
        """
        Send a list of secutity types that the algorithm trades to the browser to show the market clock - is this market open or closed!
        
        :param types: List of security types
        """
        ...

    def SendFinalResult(self) -> None:
        """
        Send a final analysis result back to the IDE.
        
        This method is protected.
        """
        ...

    def SendStatusUpdate(self, status: QuantConnect.AlgorithmStatus, message: str = ...) -> None:
        """
        Send a algorithm status update to the user of the algorithms running state.
        
        :param status: Status enum of the algorithm.
        :param message: Optional string message describing reason for status change.
        """
        ...

    def SetAlgorithm(self, algorithm: QuantConnect.Interfaces.IAlgorithm, startingPortfolioValue: float) -> None:
        """
        Set the algorithm of the result handler after its been initialized.
        
        :param algorithm: Algorithm object matching IAlgorithm interface
        :param startingPortfolioValue: Algorithm starting capital for statistics calculations
        """
        ...

    def SetNextStatusUpdate(self) -> None:
        """
        Assigns the next earliest status update time
        
        This method is protected.
        """
        ...

    def SetSummaryStatistic(self, name: str, value: str) -> None:
        """
        Sets or updates a custom summary statistic
        
        :param name: The statistic name
        :param value: The statistic value
        """
        ...

    def StatisticsResults(self) -> QuantConnect.Statistics.StatisticsResults:
        """
        Calculates and gets the current statistics for the algorithm
        
        :returns: The current statistics.
        """
        ...

    def StoreOrderEvents(self, utcTime: typing.Union[datetime.datetime, datetime.date], orderEvents: System.Collections.Generic.List[QuantConnect.Orders.OrderEvent]) -> None:
        """
        Stores the order events
        
        This method is protected.
        
        :param utcTime: The utc date associated with these order events
        :param orderEvents: The order events to store
        """
        ...

    def StoreResult(self, packet: QuantConnect.Packets.Packet) -> None:
        """
        Save the snapshot of the total results to storage.
        
        This method is protected.
        
        :param packet: Packet to store.
        """
        ...

    def SystemDebugMessage(self, message: str) -> None:
        """
        Send a live trading system debug message to the live console.
        
        :param message: Message we'd like shown in console.
        """
        ...


