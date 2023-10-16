from typing import overload
import typing

import QuantConnect
import QuantConnect.Brokerages
import QuantConnect.Brokerages.Backtesting
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Packets
import QuantConnect.Securities
import System.Collections.Generic


class BacktestingBrokerageFactory(QuantConnect.Brokerages.BrokerageFactory):
    """Factory type for the BacktestingBrokerage"""

    @property
    def BrokerageData(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Gets the brokerage data required to run the IB brokerage from configuration"""
        ...

    def __init__(self) -> None:
        """Initializes a new instance of the BacktestingBrokerageFactory class"""
        ...

    def CreateBrokerage(self, job: QuantConnect.Packets.LiveNodePacket, algorithm: QuantConnect.Interfaces.IAlgorithm) -> QuantConnect.Interfaces.IBrokerage:
        """
        Creates a new IBrokerage instance
        
        :param job: The job packet to create the brokerage for
        :param algorithm: The algorithm instance
        :returns: A new brokerage instance.
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def GetBrokerageModel(self, orderProvider: QuantConnect.Securities.IOrderProvider) -> QuantConnect.Brokerages.IBrokerageModel:
        """
        Gets a new instance of the InteractiveBrokersBrokerageModel
        
        :param orderProvider: The order provider
        """
        ...


class BacktestingBrokerage(QuantConnect.Brokerages.Brokerage):
    """Represents a brokerage to be used during backtesting. This is intended to be only be used with the BacktestingTransactionHandler"""

    @property
    def Algorithm(self) -> QuantConnect.Interfaces.IAlgorithm:
        """
        This is the algorithm under test
        
        This field is protected.
        """
        ...

    @property
    def IsConnected(self) -> bool:
        """Gets the connection status"""
        ...

    @overload
    def __init__(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        """
        Creates a new BacktestingBrokerage for the specified algorithm
        
        :param algorithm: The algorithm instance
        """
        ...

    @overload
    def __init__(self, algorithm: QuantConnect.Interfaces.IAlgorithm, name: str) -> None:
        """
        Creates a new BacktestingBrokerage for the specified algorithm
        
        This method is protected.
        
        :param algorithm: The algorithm instance
        :param name: The name of the brokerage
        """
        ...

    def CancelOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Cancels the order with the specified ID
        
        :param order: The order to cancel
        :returns: True if the request was made for the order to be canceled, false otherwise.
        """
        ...

    def Connect(self) -> None:
        """The BacktestingBrokerage is always connected. This is a no-op."""
        ...

    def Disconnect(self) -> None:
        """The BacktestingBrokerage is always connected. This is a no-op."""
        ...

    def GetAccountHoldings(self) -> System.Collections.Generic.List[QuantConnect.Holding]:
        """
        Gets all holdings for the account
        
        :returns: The current holdings from the account.
        """
        ...

    def GetCashBalance(self) -> System.Collections.Generic.List[QuantConnect.Securities.CashAmount]:
        """
        Gets the current cash balance for each currency held in the brokerage account
        
        :returns: The current cash balance for each currency available for trading.
        """
        ...

    def GetOpenOrders(self) -> System.Collections.Generic.List[QuantConnect.Orders.Order]:
        """
        Gets all open orders on the account
        
        :returns: The open orders returned from IB.
        """
        ...

    def OnOrderEvents(self, orderEvents: System.Collections.Generic.List[QuantConnect.Orders.OrderEvent]) -> None:
        """
        Event invocator for the OrderFilled event
        
        This method is protected.
        
        :param orderEvents: The list of order events
        """
        ...

    def PlaceOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Places a new order and assigns a new broker ID to the order
        
        :param order: The order to be placed
        :returns: True if the request for a new order has been placed, false otherwise.
        """
        ...

    def ProcessDelistings(self, delistings: QuantConnect.Data.Market.Delistings) -> None:
        """
        Process delistings
        
        :param delistings: Delistings to process
        """
        ...

    def Scan(self) -> None:
        """Scans all the outstanding orders and applies the algorithm model fills to generate the order events"""
        ...

    def UpdateOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Updates the order with the same ID
        
        :param order: The new order information
        :returns: True if the request was made for the order to be updated, false otherwise.
        """
        ...


