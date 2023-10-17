from typing import overload
import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Securities
import QuantConnect.Statistics
import System
import System.Collections.Generic


class Trade(System.Object):
    """Represents a closed trade"""

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        """The symbol of the traded instrument"""
        ...

    @property
    def EntryTime(self) -> datetime.datetime:
        """The date and time the trade was opened"""
        ...

    @property
    def EntryPrice(self) -> float:
        """The price at which the trade was opened (or the average price if multiple entries)"""
        ...

    @property
    def Direction(self) -> int:
        """
        The direction of the trade (Long or Short)
        
        This property contains the int value of a member of the QuantConnect.Statistics.TradeDirection enum.
        """
        ...

    @property
    def Quantity(self) -> float:
        """The total unsigned quantity of the trade"""
        ...

    @property
    def ExitTime(self) -> datetime.datetime:
        """The date and time the trade was closed"""
        ...

    @property
    def ExitPrice(self) -> float:
        """The price at which the trade was closed (or the average price if multiple exits)"""
        ...

    @property
    def ProfitLoss(self) -> float:
        """The gross profit/loss of the trade (as account currency)"""
        ...

    @property
    def TotalFees(self) -> float:
        """The total fees associated with the trade (always positive value) (as account currency)"""
        ...

    @property
    def MAE(self) -> float:
        """The Maximum Adverse Excursion (as account currency)"""
        ...

    @property
    def MFE(self) -> float:
        """The Maximum Favorable Excursion (as account currency)"""
        ...

    @property
    def Duration(self) -> datetime.timedelta:
        """Returns the duration of the trade"""
        ...

    @property
    def EndTradeDrawdown(self) -> float:
        """Returns the amount of profit given back before the trade was closed"""
        ...

    @property
    def IsWin(self) -> bool:
        """Returns whether the trade was profitable (is a win) or not (a loss)"""
        ...


class TradeStatistics(System.Object):
    """The TradeStatistics class represents a set of statistics calculated from a list of closed trades"""

    @property
    def StartDateTime(self) -> typing.Optional[datetime.datetime]:
        """The entry date/time of the first trade"""
        ...

    @property
    def EndDateTime(self) -> typing.Optional[datetime.datetime]:
        """The exit date/time of the last trade"""
        ...

    @property
    def TotalNumberOfTrades(self) -> int:
        """The total number of trades"""
        ...

    @property
    def NumberOfWinningTrades(self) -> int:
        """The total number of winning trades"""
        ...

    @property
    def NumberOfLosingTrades(self) -> int:
        """The total number of losing trades"""
        ...

    @property
    def TotalProfitLoss(self) -> float:
        """The total profit/loss for all trades (as symbol currency)"""
        ...

    @property
    def TotalProfit(self) -> float:
        """The total profit for all winning trades (as symbol currency)"""
        ...

    @property
    def TotalLoss(self) -> float:
        """The total loss for all losing trades (as symbol currency)"""
        ...

    @property
    def LargestProfit(self) -> float:
        """The largest profit in a single trade (as symbol currency)"""
        ...

    @property
    def LargestLoss(self) -> float:
        """The largest loss in a single trade (as symbol currency)"""
        ...

    @property
    def AverageProfitLoss(self) -> float:
        """The average profit/loss (a.k.a. Expectancy or Average Trade) for all trades (as symbol currency)"""
        ...

    @property
    def AverageProfit(self) -> float:
        """The average profit for all winning trades (as symbol currency)"""
        ...

    @property
    def AverageLoss(self) -> float:
        """The average loss for all winning trades (as symbol currency)"""
        ...

    @property
    def AverageTradeDuration(self) -> datetime.timedelta:
        """The average duration for all trades"""
        ...

    @property
    def AverageWinningTradeDuration(self) -> datetime.timedelta:
        """The average duration for all winning trades"""
        ...

    @property
    def AverageLosingTradeDuration(self) -> datetime.timedelta:
        """The average duration for all losing trades"""
        ...

    @property
    def MedianTradeDuration(self) -> datetime.timedelta:
        """The median duration for all trades"""
        ...

    @property
    def MedianWinningTradeDuration(self) -> datetime.timedelta:
        """The median duration for all winning trades"""
        ...

    @property
    def MedianLosingTradeDuration(self) -> datetime.timedelta:
        """The median duration for all losing trades"""
        ...

    @property
    def MaxConsecutiveWinningTrades(self) -> int:
        """The maximum number of consecutive winning trades"""
        ...

    @property
    def MaxConsecutiveLosingTrades(self) -> int:
        """The maximum number of consecutive losing trades"""
        ...

    @property
    def ProfitLossRatio(self) -> float:
        """The ratio of the average profit per trade to the average loss per trade"""
        ...

    @property
    def WinLossRatio(self) -> float:
        """The ratio of the number of winning trades to the number of losing trades"""
        ...

    @property
    def WinRate(self) -> float:
        """The ratio of the number of winning trades to the total number of trades"""
        ...

    @property
    def LossRate(self) -> float:
        """The ratio of the number of losing trades to the total number of trades"""
        ...

    @property
    def AverageMAE(self) -> float:
        """The average Maximum Adverse Excursion for all trades"""
        ...

    @property
    def AverageMFE(self) -> float:
        """The average Maximum Favorable Excursion for all trades"""
        ...

    @property
    def LargestMAE(self) -> float:
        """The largest Maximum Adverse Excursion in a single trade (as symbol currency)"""
        ...

    @property
    def LargestMFE(self) -> float:
        """The largest Maximum Favorable Excursion in a single trade (as symbol currency)"""
        ...

    @property
    def MaximumClosedTradeDrawdown(self) -> float:
        """The maximum closed-trade drawdown for all trades (as symbol currency)"""
        ...

    @property
    def MaximumIntraTradeDrawdown(self) -> float:
        """The maximum intra-trade drawdown for all trades (as symbol currency)"""
        ...

    @property
    def ProfitLossStandardDeviation(self) -> float:
        """The standard deviation of the profits/losses for all trades (as symbol currency)"""
        ...

    @property
    def ProfitLossDownsideDeviation(self) -> float:
        """The downside deviation of the profits/losses for all trades (as symbol currency)"""
        ...

    @property
    def ProfitFactor(self) -> float:
        """The ratio of the total profit to the total loss"""
        ...

    @property
    def SharpeRatio(self) -> float:
        """The ratio of the average profit/loss to the standard deviation"""
        ...

    @property
    def SortinoRatio(self) -> float:
        """The ratio of the average profit/loss to the downside deviation"""
        ...

    @property
    def ProfitToMaxDrawdownRatio(self) -> float:
        """The ratio of the total profit/loss to the maximum closed trade drawdown"""
        ...

    @property
    def MaximumEndTradeDrawdown(self) -> float:
        """The maximum amount of profit given back by a single trade before exit (as symbol currency)"""
        ...

    @property
    def AverageEndTradeDrawdown(self) -> float:
        """The average amount of profit given back by all trades before exit (as symbol currency)"""
        ...

    @property
    def MaximumDrawdownDuration(self) -> datetime.timedelta:
        """The maximum amount of time to recover from a drawdown (longest time between new equity highs or peaks)"""
        ...

    @property
    def TotalFees(self) -> float:
        """The sum of fees for all trades"""
        ...

    @overload
    def __init__(self, trades: System.Collections.Generic.IEnumerable[QuantConnect.Statistics.Trade]) -> None:
        """
        Initializes a new instance of the TradeStatistics class
        
        :param trades: The list of closed trades
        """
        ...

    @overload
    def __init__(self) -> None:
        """Initializes a new instance of the TradeStatistics class"""
        ...


class Statistics(System.Object):
    """Calculate all the statistics required from the backtest, based on the equity curve and the profit loss statement."""

    @staticmethod
    def AnnualPerformance(performance: System.Collections.Generic.List[float], tradingDaysPerYear: float = 252) -> float:
        """
        Annualized return statistic calculated as an average of daily trading performance multiplied by the number of trading days per year.
        
        :param performance: Dictionary collection of double performance values
        :param tradingDaysPerYear: Trading days per year for the assets in portfolio
        :returns: Double annual performance percentage.
        """
        ...

    @staticmethod
    def AnnualStandardDeviation(performance: System.Collections.Generic.List[float], tradingDaysPerYear: float = 252) -> float:
        """
        Annualized standard deviation
        
        :param performance: Collection of double values for daily performance
        :param tradingDaysPerYear: Number of trading days for the assets in portfolio to get annualize standard deviation.
        :returns: Value for annual standard deviation.
        """
        ...

    @staticmethod
    def AnnualVariance(performance: System.Collections.Generic.List[float], tradingDaysPerYear: float = 252) -> float:
        """
        Annualized variance statistic calculation using the daily performance variance and trading days per year.
        
        :returns: Annual variance value.
        """
        ...

    @staticmethod
    def CompoundingAnnualPerformance(startingCapital: float, finalCapital: float, years: float) -> float:
        """
        Annual compounded returns statistic based on the final-starting capital and years.
        
        :param startingCapital: Algorithm starting capital
        :param finalCapital: Algorithm final capital
        :param years: Years trading
        :returns: Decimal fraction for annual compounding performance.
        """
        ...

    @staticmethod
    @overload
    def DrawdownPercent(equityOverTime: System.Collections.Generic.SortedDictionary[datetime.datetime, float], rounding: int = 2) -> float:
        """Drawdown maximum percentage."""
        ...

    @staticmethod
    @overload
    def DrawdownPercent(current: float, high: float, roundingDecimals: int = 2) -> float:
        """
        Calculate the drawdown between a high and current value
        
        :param current: Current value
        :param high: Latest maximum
        :param roundingDecimals: Digits to round the result too
        :returns: Drawdown percentage.
        """
        ...

    @staticmethod
    def ObservedSharpeRatio(listPerformance: System.Collections.Generic.List[float]) -> float:
        """
        Calculates the observed sharpe ratio
        
        :param listPerformance: The performance samples to use
        :returns: The observed sharpe ratio.
        """
        ...

    @staticmethod
    def ProbabilisticSharpeRatio(listPerformance: System.Collections.Generic.List[float], benchmarkSharpeRatio: float) -> float:
        """
        Helper method to calculate the probabilistic sharpe ratio
        
        :param listPerformance: The list of algorithm performance values
        :param benchmarkSharpeRatio: The benchmark sharpe ratio to use
        :returns: Probabilistic Sharpe Ratio.
        """
        ...

    @staticmethod
    def SharpeRatio(algoPerformance: System.Collections.Generic.List[float], riskFreeRate: float) -> float:
        """
        Sharpe ratio with respect to risk free rate: measures excess of return per unit of risk.
        
        :param algoPerformance: Collection of double values for the algorithm daily performance
        :returns: Value for sharpe ratio.
        """
        ...

    @staticmethod
    def TrackingError(algoPerformance: System.Collections.Generic.List[float], benchmarkPerformance: System.Collections.Generic.List[float], tradingDaysPerYear: float = 252) -> float:
        """
        Tracking error volatility (TEV) statistic - a measure of how closely a portfolio follows the index to which it is benchmarked
        
        :param algoPerformance: Double collection of algorithm daily performance values
        :param benchmarkPerformance: Double collection of benchmark daily performance values
        :param tradingDaysPerYear: Number of trading days per year
        :returns: Value for tracking error.
        """
        ...


class PortfolioStatistics(System.Object):
    """The PortfolioStatistics class represents a set of statistics calculated from equity and benchmark samples"""

    @property
    def AverageWinRate(self) -> float:
        """The average rate of return for winning trades"""
        ...

    @property
    def AverageLossRate(self) -> float:
        """The average rate of return for losing trades"""
        ...

    @property
    def ProfitLossRatio(self) -> float:
        """The ratio of the average win rate to the average loss rate"""
        ...

    @property
    def WinRate(self) -> float:
        """The ratio of the number of winning trades to the total number of trades"""
        ...

    @property
    def LossRate(self) -> float:
        """The ratio of the number of losing trades to the total number of trades"""
        ...

    @property
    def Expectancy(self) -> float:
        """The expected value of the rate of return"""
        ...

    @property
    def CompoundingAnnualReturn(self) -> float:
        """Annual compounded returns statistic based on the final-starting capital and years."""
        ...

    @property
    def Drawdown(self) -> float:
        """Drawdown maximum percentage."""
        ...

    @property
    def TotalNetProfit(self) -> float:
        """The total net profit percentage."""
        ...

    @property
    def SharpeRatio(self) -> float:
        """Sharpe ratio with respect to risk free rate: measures excess of return per unit of risk."""
        ...

    @property
    def ProbabilisticSharpeRatio(self) -> float:
        """
        Probabilistic Sharpe Ratio is a probability measure associated with the Sharpe ratio.
        It informs us of the probability that the estimated Sharpe ratio is greater than a chosen benchmark
        """
        ...

    @property
    def Alpha(self) -> float:
        """Algorithm "Alpha" statistic - abnormal returns over the risk free rate and the relationshio (beta) with the benchmark returns."""
        ...

    @property
    def Beta(self) -> float:
        """Algorithm "beta" statistic - the covariance between the algorithm and benchmark performance, divided by benchmark's variance"""
        ...

    @property
    def AnnualStandardDeviation(self) -> float:
        """Annualized standard deviation"""
        ...

    @property
    def AnnualVariance(self) -> float:
        """Annualized variance statistic calculation using the daily performance variance and trading days per year."""
        ...

    @property
    def InformationRatio(self) -> float:
        """Information ratio - risk adjusted return"""
        ...

    @property
    def TrackingError(self) -> float:
        """Tracking error volatility (TEV) statistic - a measure of how closely a portfolio follows the index to which it is benchmarked"""
        ...

    @property
    def TreynorRatio(self) -> float:
        """Treynor ratio statistic is a measurement of the returns earned in excess of that which could have been earned on an investment that has no diversifiable risk"""
        ...

    @property
    def PortfolioTurnover(self) -> float:
        """The average Portfolio Turnover"""
        ...

    @overload
    def __init__(self, profitLoss: System.Collections.Generic.SortedDictionary[datetime.datetime, float], equity: System.Collections.Generic.SortedDictionary[datetime.datetime, float], portfolioTurnover: System.Collections.Generic.SortedDictionary[datetime.datetime, float], listPerformance: System.Collections.Generic.List[float], listBenchmark: System.Collections.Generic.List[float], startingCapital: float, tradingDaysPerYear: int = 252, winCount: typing.Optional[int] = None, lossCount: typing.Optional[int] = None) -> None:
        """
        Initializes a new instance of the PortfolioStatistics class
        
        :param profitLoss: Trade record of profits and losses
        :param equity: The list of daily equity values
        :param portfolioTurnover: The algorithm portfolio turnover
        :param listPerformance: The list of algorithm performance values
        :param listBenchmark: The list of benchmark values
        :param startingCapital: The algorithm starting capital
        :param tradingDaysPerYear: The number of trading days per year
        :param winCount: The number of wins, including ITM options with profitLoss less than 0. If this and  are null, they will be calculated from
        :param lossCount: The number of losses
        """
        ...

    @overload
    def __init__(self) -> None:
        """Initializes a new instance of the PortfolioStatistics class"""
        ...

    @staticmethod
    def GetAverageRiskFreeRate(dates: System.Collections.Generic.IEnumerable[datetime.datetime]) -> float:
        """
        Gets the average Risk Free Rate from the interest rate of the given dates
        
        :param dates: Collection of dates from which the interest rates will be computed and then the average of them
        """
        ...

    @staticmethod
    def GetRiskFreeRate(startDate: typing.Union[datetime.datetime, datetime.date], endDate: typing.Union[datetime.datetime, datetime.date]) -> float:
        """
        Gets the average risk free annual return rate
        
        :param startDate: Start date to calculate the average
        :param endDate: End date to calculate the average
        """
        ...


class AlgorithmPerformance(System.Object):
    """The AlgorithmPerformance class is a wrapper for TradeStatistics and PortfolioStatistics"""

    @property
    def TradeStatistics(self) -> QuantConnect.Statistics.TradeStatistics:
        """The algorithm statistics on closed trades"""
        ...

    @property
    def PortfolioStatistics(self) -> QuantConnect.Statistics.PortfolioStatistics:
        """The algorithm statistics on portfolio"""
        ...

    @property
    def ClosedTrades(self) -> System.Collections.Generic.List[QuantConnect.Statistics.Trade]:
        """The list of closed trades"""
        ...

    @overload
    def __init__(self, trades: System.Collections.Generic.List[QuantConnect.Statistics.Trade], profitLoss: System.Collections.Generic.SortedDictionary[datetime.datetime, float], equity: System.Collections.Generic.SortedDictionary[datetime.datetime, float], portfolioTurnover: System.Collections.Generic.SortedDictionary[datetime.datetime, float], listPerformance: System.Collections.Generic.List[float], listBenchmark: System.Collections.Generic.List[float], startingCapital: float, winningTransactions: int, losingTransactions: int) -> None:
        """
        Initializes a new instance of the AlgorithmPerformance class
        
        :param trades: The list of closed trades
        :param profitLoss: Trade record of profits and losses
        :param equity: The list of daily equity values
        :param portfolioTurnover: The algorithm portfolio turnover
        :param listPerformance: The list of algorithm performance values
        :param listBenchmark: The list of benchmark values
        :param startingCapital: The algorithm starting capital
        :param winningTransactions: Number of winning transactions
        :param losingTransactions: Number of losing transactions
        """
        ...

    @overload
    def __init__(self) -> None:
        """Initializes a new instance of the AlgorithmPerformance class"""
        ...


class StatisticsResults(System.Object):
    """The StatisticsResults class represents total and rolling statistics for an algorithm"""

    @property
    def TotalPerformance(self) -> QuantConnect.Statistics.AlgorithmPerformance:
        """The performance of the algorithm over the whole period"""
        ...

    @property
    def RollingPerformances(self) -> System.Collections.Generic.Dictionary[str, QuantConnect.Statistics.AlgorithmPerformance]:
        """The rolling performance of the algorithm over 1, 3, 6, 12 month periods"""
        ...

    @property
    def Summary(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Returns a summary of the algorithm performance as a dictionary"""
        ...

    @overload
    def __init__(self, totalPerformance: QuantConnect.Statistics.AlgorithmPerformance, rollingPerformances: System.Collections.Generic.Dictionary[str, QuantConnect.Statistics.AlgorithmPerformance], summary: System.Collections.Generic.Dictionary[str, str]) -> None:
        """
        Initializes a new instance of the StatisticsResults class
        
        :param totalPerformance: The algorithm total performance
        :param rollingPerformances: The algorithm rolling performances
        :param summary: The summary performance dictionary
        """
        ...

    @overload
    def __init__(self) -> None:
        """Initializes a new instance of the StatisticsResults class"""
        ...


class StatisticsBuilder(System.Object):
    """The StatisticsBuilder class creates summary and rolling statistics from trades, equity and benchmark points"""

    @staticmethod
    def CreateBenchmarkDifferences(points: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[datetime.datetime, float]], fromDate: typing.Union[datetime.datetime, datetime.date], toDate: typing.Union[datetime.datetime, datetime.date]) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[datetime.datetime, float]]:
        """
        Yields pairs of date and percentage change for the period
        
        :param points: The values to calculate percentage change for
        :param fromDate: Starting date (inclusive)
        :param toDate: Ending date (inclusive)
        :returns: Pairs of date and percentage change.
        """
        ...

    @staticmethod
    def Generate(trades: System.Collections.Generic.List[QuantConnect.Statistics.Trade], profitLoss: System.Collections.Generic.SortedDictionary[datetime.datetime, float], pointsEquity: System.Collections.Generic.List[QuantConnect.ISeriesPoint], pointsPerformance: System.Collections.Generic.List[QuantConnect.ISeriesPoint], pointsBenchmark: System.Collections.Generic.List[QuantConnect.ISeriesPoint], pointsPortfolioTurnover: System.Collections.Generic.List[QuantConnect.ISeriesPoint], startingCapital: float, totalFees: float, totalTransactions: int, estimatedStrategyCapacity: QuantConnect.CapacityEstimate, accountCurrencySymbol: str, transactions: QuantConnect.Securities.SecurityTransactionManager) -> QuantConnect.Statistics.StatisticsResults:
        """
        Generates the statistics and returns the results
        
        :param trades: The list of closed trades
        :param profitLoss: Trade record of profits and losses
        :param pointsEquity: The list of daily equity values
        :param pointsPerformance: The list of algorithm performance values
        :param pointsBenchmark: The list of benchmark values
        :param pointsPortfolioTurnover: The list of portfolio turnover daily samples
        :param startingCapital: The algorithm starting capital
        :param totalFees: The total fees
        :param totalTransactions: The total number of transactions
        :param estimatedStrategyCapacity: The estimated capacity of this strategy
        :param accountCurrencySymbol: The account currency symbol
        :param transactions: The transaction manager to get number of winning and losing transactions
        :returns: Returns a StatisticsResults object.
        """
        ...

    @staticmethod
    def PreprocessPerformanceValues(points: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[datetime.datetime, float]]) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[datetime.datetime, float]]:
        """
        Skips the first two entries from the given points and divides each entry by 100
        
        :param points: The values to divide by 100
        :returns: Pairs of date and performance value divided by 100.
        """
        ...


class PerformanceMetrics(System.Object):
    """PerformanceMetrics contains the names of the various performance metrics used for evaluation purposes."""

    Alpha: str = "Alpha"

    AnnualStandardDeviation: str = "Annual Standard Deviation"

    AnnualVariance: str = "Annual Variance"

    AverageLoss: str = "Average Loss"

    AverageWin: str = "Average Win"

    Beta: str = "Beta"

    CompoundingAnnualReturn: str = "Compounding Annual Return"

    Drawdown: str = "Drawdown"

    EstimatedStrategyCapacity: str = "Estimated Strategy Capacity"

    Expectancy: str = "Expectancy"

    InformationRatio: str = "Information Ratio"

    LossRate: str = "Loss Rate"

    NetProfit: str = "Net Profit"

    ProbabilisticSharpeRatio: str = "Probabilistic Sharpe Ratio"

    ProfitLossRatio: str = "Profit-Loss Ratio"

    SharpeRatio: str = "Sharpe Ratio"

    TotalFees: str = "Total Fees"

    TotalTrades: str = "Total Trades"

    TrackingError: str = "Tracking Error"

    TreynorRatio: str = "Treynor Ratio"

    WinRate: str = "Win Rate"

    LowestCapacityAsset: str = "Lowest Capacity Asset"

    PortfolioTurnover: str = "Portfolio Turnover"


class IStatisticsService(metaclass=abc.ABCMeta):
    """This interface exposes methods for accessing algorithm statistics results at runtime."""


class FillGroupingMethod(System.Enum):
    """The method used to group order fills into trades"""

    FillToFill = 0
    """A Trade is defined by a fill that establishes or increases a position and an offsetting fill that reduces the position size (0)"""

    FlatToFlat = 1
    """A Trade is defined by a sequence of fills, from a flat position to a non-zero position which may increase or decrease in quantity, and back to a flat position (1)"""

    FlatToReduced = 2
    """A Trade is defined by a sequence of fills, from a flat position to a non-zero position and an offsetting fill that reduces the position size (2)"""


class FillMatchingMethod(System.Enum):
    """The method used to match offsetting order fills"""

    FIFO = 0
    """First In First Out fill matching method (0)"""

    LIFO = 1
    """Last In Last Out fill matching method (1)"""


class TradeBuilder(System.Object, QuantConnect.Interfaces.ITradeBuilder):
    """The TradeBuilder class generates trades from executions and market price updates"""

    @property
    def ClosedTrades(self) -> System.Collections.Generic.List[QuantConnect.Statistics.Trade]:
        """The list of closed trades"""
        ...

    def __init__(self, groupingMethod: QuantConnect.Statistics.FillGroupingMethod, matchingMethod: QuantConnect.Statistics.FillMatchingMethod) -> None:
        """Initializes a new instance of the TradeBuilder class"""
        ...

    def ApplySplit(self, split: QuantConnect.Data.Market.Split, liveMode: bool, dataNormalizationMode: QuantConnect.DataNormalizationMode) -> None:
        """
        Applies a split to the trade builder
        
        :param split: The split to be applied
        :param liveMode: True if live mode, false for backtest
        :param dataNormalizationMode: The DataNormalizationMode for this security
        """
        ...

    def HasOpenPosition(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Returns true if there is an open position for the symbol
        
        :param symbol: The symbol
        :returns: true if there is an open position for the symbol.
        """
        ...

    def ProcessFill(self, fill: QuantConnect.Orders.OrderEvent, conversionRate: float, feeInAccountCurrency: float, multiplier: float = 1.0) -> None:
        """
        Processes a new fill, eventually creating new trades
        
        :param fill: The new fill order event
        :param conversionRate: The current security market conversion rate into the account currency
        :param feeInAccountCurrency: The current order fee in the account currency
        :param multiplier: The contract multiplier
        """
        ...

    def SetLiveMode(self, live: bool) -> None:
        """
        Sets the live mode flag
        
        :param live: The live mode flag
        """
        ...

    def SetMarketPrice(self, symbol: typing.Union[QuantConnect.Symbol, str], price: float) -> None:
        """Sets the current market price for the symbol"""
        ...

    def SetSecurityManager(self, securities: QuantConnect.Securities.SecurityManager) -> None:
        """
        Sets the security manager instance
        
        :param securities: The security manager
        """
        ...


class TradeDirection(System.Enum):
    """Direction of a trade"""

    Long = 0
    """Long direction (0)"""

    Short = 1
    """Short direction (1)"""


