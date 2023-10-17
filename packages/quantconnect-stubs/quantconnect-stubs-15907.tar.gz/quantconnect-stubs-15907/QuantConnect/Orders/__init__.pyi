from typing import overload
import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Algorithm.Framework.Portfolio
import QuantConnect.Api
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Orders.Fees
import QuantConnect.Orders.Serialization
import QuantConnect.Securities
import QuantConnect.Securities.Positions
import System
import System.Collections.Generic
import System.Threading

JsonConverter = typing.Any

QuantConnect_Orders_OrderTicket_Get_T = typing.TypeVar("QuantConnect_Orders_OrderTicket_Get_T")


class OrderRequestStatus(System.Enum):
    """Specifies the status of a request"""

    Unprocessed = 0
    """This is an unprocessed request (0)"""

    Processing = 1
    """This request is partially processed (1)"""

    Processed = 2
    """This request has been completely processed (2)"""

    Error = 3
    """This request encountered an error (3)"""


class OrderRequest(System.Object, metaclass=abc.ABCMeta):
    """Represents a request to submit, update, or cancel an order"""

    @property
    @abc.abstractmethod
    def OrderRequestType(self) -> int:
        """
        Gets the type of this order request
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderRequestType enum.
        """
        ...

    @property
    def Status(self) -> int:
        """
        Gets the status of this request
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderRequestStatus enum.
        """
        ...

    @property
    def Time(self) -> datetime.datetime:
        """Gets the UTC time the request was created"""
        ...

    @property
    def OrderId(self) -> int:
        """Gets the order id the request acts on"""
        ...

    @property
    def Tag(self) -> str:
        """Gets a tag for this request"""
        ...

    @property
    def Response(self) -> QuantConnect.Orders.OrderResponse:
        """
        Gets the response for this request. If this request was never processed then this
        will equal OrderResponse.Unprocessed. This value is never equal to null.
        """
        ...

    def __init__(self, time: typing.Union[datetime.datetime, datetime.date], orderId: int, tag: str) -> None:
        """
        Initializes a new instance of the OrderRequest class
        
        This method is protected.
        
        :param time: The time this request was created
        :param orderId: The order id this request acts on, specify zero for SubmitOrderRequest
        :param tag: A custom tag for the request
        """
        ...

    def SetResponse(self, response: QuantConnect.Orders.OrderResponse, status: QuantConnect.Orders.OrderRequestStatus = ...) -> None:
        """
        Sets the Response for this request
        
        :param response: The response to this request
        :param status: The current status of this request
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class OrderResponseErrorCode(System.Enum):
    """Error detail code"""

    # Cannot convert to Python: None = 0
    """No error (0)"""

    ProcessingError = -1
    """Unknown error (-1)"""

    OrderAlreadyExists = -2
    """Cannot submit because order already exists (-2)"""

    InsufficientBuyingPower = -3
    """Not enough money to to submit order (-3)"""

    BrokerageModelRefusedToSubmitOrder = -4
    """Internal logic invalidated submit order (-4)"""

    BrokerageFailedToSubmitOrder = -5
    """Brokerage submit error (-5)"""

    BrokerageFailedToUpdateOrder = -6
    """Brokerage update error (-6)"""

    BrokerageHandlerRefusedToUpdateOrder = -7
    """Internal logic invalidated update order (-7)"""

    BrokerageFailedToCancelOrder = -8
    """Brokerage cancel error (-8)"""

    InvalidOrderStatus = -9
    """Only pending orders can be canceled (-9)"""

    UnableToFindOrder = -10
    """Missing order (-10)"""

    OrderQuantityZero = -11
    """Cannot submit or update orders with zero quantity (-11)"""

    UnsupportedRequestType = -12
    """This type of request is unsupported (-12)"""

    PreOrderChecksError = -13
    """Unknown error during pre order request validation (-13)"""

    MissingSecurity = -14
    """Security is missing. Probably did not subscribe (-14)"""

    ExchangeNotOpen = -15
    """Some order types require open exchange (-15)"""

    SecurityPriceZero = -16
    """Zero security price is probably due to bad data (-16)"""

    ForexBaseAndQuoteCurrenciesRequired = -17
    """Need both currencies in cashbook to trade a pair (-17)"""

    ForexConversionRateZero = -18
    """Need conversion rate to account currency (-18)"""

    SecurityHasNoData = -19
    """Should not attempt trading without at least one data point (-19)"""

    ExceededMaximumOrders = -20
    """Transaction manager's cache is full (-20)"""

    MarketOnCloseOrderTooLate = -21
    """Below buffer time for MOC order to be placed before exchange closes. 15.5 minutes by default (-21)"""

    InvalidRequest = -22
    """Request is invalid or null (-22)"""

    RequestCanceled = -23
    """Request was canceled by user (-23)"""

    AlgorithmWarmingUp = -24
    """All orders are invalidated while algorithm is warming up (-24)"""

    BrokerageModelRefusedToUpdateOrder = -25
    """Internal logic invalidated update order (-25)"""

    QuoteCurrencyRequired = -26
    """Need quote currency in cashbook to trade (-26)"""

    ConversionRateZero = -27
    """Need conversion rate to account currency (-27)"""

    NonTradableSecurity = -28
    """The order's symbol references a non-tradable security (-28)"""

    NonExercisableSecurity = -29
    """The order's symbol references a non-exercisable security (-29)"""

    OrderQuantityLessThanLotSize = -30
    """Cannot submit or update orders with quantity that is less than lot size (-30)"""

    ExceedsShortableQuantity = -31
    """The order's quantity exceeds the max shortable quantity set by the brokerage (-31)"""

    InvalidNewOrderStatus = -32
    """Cannot update/cancel orders with OrderStatus.New (-32)"""

    EuropeanOptionNotExpiredOnExercise = -33
    """Exercise time before expiry for European options (-33)"""


class TimeInForce(System.Object, QuantConnect.Interfaces.ITimeInForceHandler, metaclass=abc.ABCMeta):
    """Time In Force - defines the length of time over which an order will continue working before it is canceled"""

    GoodTilCanceled: QuantConnect.Orders.TimeInForce = ...
    """Gets a GoodTilCanceledTimeInForce instance"""

    Day: QuantConnect.Orders.TimeInForce = ...
    """Gets a DayTimeInForce instance"""

    @staticmethod
    def GoodTilDate(expiry: typing.Union[datetime.datetime, datetime.date]) -> QuantConnect.Orders.TimeInForce:
        """Gets a GoodTilDateTimeInForce instance"""
        ...

    def IsFillValid(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, fill: QuantConnect.Orders.OrderEvent) -> bool:
        """
        Checks if an order fill is valid
        
        :param security: The security matching the order
        :param order: The order to be checked
        :param fill: The order fill to be checked
        :returns: Returns true if the order fill can be emitted, false otherwise.
        """
        ...

    def IsOrderExpired(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order) -> bool:
        """
        Checks if an order is expired
        
        :param security: The security matching the order
        :param order: The order to be checked
        :returns: Returns true if the order has expired, false otherwise.
        """
        ...


class OrderSubmissionData(System.Object):
    """
    The purpose of this class is to store time and price information
    available at the time an order was submitted.
    """

    @property
    def BidPrice(self) -> float:
        """The bid price at order submission time"""
        ...

    @property
    def AskPrice(self) -> float:
        """The ask price at order submission time"""
        ...

    @property
    def LastPrice(self) -> float:
        """The current price at order submission time"""
        ...

    def __init__(self, bidPrice: float, askPrice: float, lastPrice: float) -> None:
        """Initializes a new instance of the OrderSubmissionData class"""
        ...

    def Clone(self) -> QuantConnect.Orders.OrderSubmissionData:
        """Return a new instance clone of this object"""
        ...


class GroupOrderManager(System.Object):
    """Manager of a group of orders"""

    @property
    def Id(self) -> int:
        """The unique order group Id"""
        ...

    @property
    def Quantity(self) -> float:
        """The group order quantity"""
        ...

    @property
    def Count(self) -> int:
        """The total order count associated with this order group"""
        ...

    @property
    def LimitPrice(self) -> float:
        """The limit price associated with this order group if any"""
        ...

    @property
    def OrderIds(self) -> System.Collections.Generic.HashSet[int]:
        """The order Ids in this group"""
        ...

    @property
    def Direction(self) -> int:
        """
        Order Direction Property based off Quantity.
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderDirection enum.
        """
        ...

    @property
    def AbsoluteQuantity(self) -> float:
        """Get the absolute quantity for this combo order"""
        ...

    @overload
    def __init__(self) -> None:
        """Creates a new empty instance"""
        ...

    @overload
    def __init__(self, id: int, legCount: int, quantity: float, limitPrice: float = 0) -> None:
        """
        Creates a new instance
        
        :param id: This order group unique Id
        :param legCount: The order leg count
        :param quantity: The group order quantity
        :param limitPrice: The limit price associated with this order group if any
        """
        ...


class UpdateOrderFields(System.Object):
    """Specifies the data in an order to be updated"""

    @property
    def Quantity(self) -> typing.Optional[float]:
        """Specify to update the quantity of the order"""
        ...

    @property
    def LimitPrice(self) -> typing.Optional[float]:
        """Specify to update the limit price of the order"""
        ...

    @property
    def StopPrice(self) -> typing.Optional[float]:
        """Specify to update the stop price of the order"""
        ...

    @property
    def TriggerPrice(self) -> typing.Optional[float]:
        """Specify to update the trigger price of the order"""
        ...

    @property
    def TrailingAmount(self) -> typing.Optional[float]:
        """The trailing stop order trailing amount"""
        ...

    @property
    def Tag(self) -> str:
        """Specify to update the order's tag"""
        ...


class UpdateOrderRequest(QuantConnect.Orders.OrderRequest):
    """Defines a request to update an order's values"""

    @property
    def OrderRequestType(self) -> int:
        """
        Gets Orders.OrderRequestType.Update
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderRequestType enum.
        """
        ...

    @property
    def Quantity(self) -> typing.Optional[float]:
        """Gets the new quantity of the order, null to not change the quantity"""
        ...

    @property
    def LimitPrice(self) -> typing.Optional[float]:
        """Gets the new limit price of the order, null to not change the limit price"""
        ...

    @property
    def StopPrice(self) -> typing.Optional[float]:
        """Gets the new stop price of the order, null to not change the stop price"""
        ...

    @property
    def TriggerPrice(self) -> typing.Optional[float]:
        """Gets the new trigger price of the order, null to not change the trigger price"""
        ...

    @property
    def TrailingAmount(self) -> typing.Optional[float]:
        """The trailing stop order trailing amount"""
        ...

    def __init__(self, time: typing.Union[datetime.datetime, datetime.date], orderId: int, fields: QuantConnect.Orders.UpdateOrderFields) -> None:
        """
        Initializes a new instance of the UpdateOrderRequest class
        
        :param time: The time the request was submitted
        :param orderId: The order id to be updated
        :param fields: The fields defining what should be updated
        """
        ...

    def IsAllowedForClosedOrder(self) -> bool:
        """
        Checks whether the update request is allowed for a closed order.
        Only tag updates are allowed on closed orders.
        
        :returns: True if the update request is allowed for a closed order.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class OrderType(System.Enum):
    """Type of the order: market, limit or stop"""

    Market = 0
    """Market Order Type (0)"""

    Limit = 1
    """Limit Order Type (1)"""

    StopMarket = 2
    """Stop Market Order Type - Fill at market price when break target price (2)"""

    StopLimit = 3
    """Stop limit order type - trigger fill once pass the stop price; but limit fill to limit price (3)"""

    MarketOnOpen = 4
    """Market on open type - executed on exchange open (4)"""

    MarketOnClose = 5
    """Market on close type - executed on exchange close (5)"""

    OptionExercise = 6
    """Option Exercise Order Type (6)"""

    LimitIfTouched = 7
    """Limit if Touched Order Type - a limit order to be placed after first reaching a trigger value (7)"""

    ComboMarket = 8
    """Combo Market Order Type - (8)"""

    ComboLimit = 9
    """Combo Limit Order Type - (9)"""

    ComboLegLimit = 10
    """Combo Leg Limit Order Type - (10)"""

    TrailingStop = 11
    """Trailing Stop Order Type - (11)"""


class SubmitOrderRequest(QuantConnect.Orders.OrderRequest):
    """Defines a request to submit a new order"""

    @property
    def OrderRequestType(self) -> int:
        """
        Gets Orders.OrderRequestType.Submit
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderRequestType enum.
        """
        ...

    @property
    def SecurityType(self) -> int:
        """
        Gets the security type of the symbol
        
        This property contains the int value of a member of the QuantConnect.SecurityType enum.
        """
        ...

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        """Gets the symbol to be traded"""
        ...

    @property
    def OrderType(self) -> int:
        """
        Gets the order type od the order
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @property
    def Quantity(self) -> float:
        """Gets the quantity of the order"""
        ...

    @property
    def LimitPrice(self) -> float:
        """Gets the limit price of the order, zero if not a limit order"""
        ...

    @property
    def StopPrice(self) -> float:
        """Gets the stop price of the order, zero if not a stop order"""
        ...

    @property
    def TriggerPrice(self) -> float:
        """Price which must first be reached before a limit order can be submitted."""
        ...

    @property
    def TrailingAmount(self) -> float:
        """Trailing amount for a trailing stop order"""
        ...

    @property
    def TrailingAsPercentage(self) -> bool:
        """Determines whether the TrailingAmount is a percentage or an absolute currency value"""
        ...

    @property
    def OrderProperties(self) -> QuantConnect.Interfaces.IOrderProperties:
        """Gets the order properties for this request"""
        ...

    @property
    def GroupOrderManager(self) -> QuantConnect.Orders.GroupOrderManager:
        """Gets the manager for the combo order. If null, the order is not a combo order."""
        ...

    @overload
    def __init__(self, orderType: QuantConnect.Orders.OrderType, securityType: QuantConnect.SecurityType, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, stopPrice: float, limitPrice: float, triggerPrice: float, trailingAmount: float, trailingAsPercentage: bool, time: typing.Union[datetime.datetime, datetime.date], tag: str, properties: QuantConnect.Interfaces.IOrderProperties = None, groupOrderManager: QuantConnect.Orders.GroupOrderManager = None) -> None:
        """
        Initializes a new instance of the SubmitOrderRequest class.
        The OrderRequest.OrderId will default to OrderResponseErrorCode.UnableToFindOrder
        
        :param orderType: The order type to be submitted
        :param securityType: The symbol's SecurityType
        :param symbol: The symbol to be traded
        :param quantity: The number of units to be ordered
        :param stopPrice: The stop price for stop orders, non-stop orders this value is ignored
        :param limitPrice: The limit price for limit orders, non-limit orders this value is ignored
        :param triggerPrice: The trigger price for limit if touched orders, for non-limit if touched orders this value is ignored
        :param trailingAmount: The trailing amount to be used to update the stop price
        :param trailingAsPercentage: Whether the  is a percentage or an absolute currency value
        :param time: The time this request was created
        :param tag: A custom tag for this request
        :param properties: The order properties for this request
        :param groupOrderManager: The manager for this combo order
        """
        ...

    @overload
    def __init__(self, orderType: QuantConnect.Orders.OrderType, securityType: QuantConnect.SecurityType, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, stopPrice: float, limitPrice: float, triggerPrice: float, time: typing.Union[datetime.datetime, datetime.date], tag: str, properties: QuantConnect.Interfaces.IOrderProperties = None, groupOrderManager: QuantConnect.Orders.GroupOrderManager = None) -> None:
        """
        Initializes a new instance of the SubmitOrderRequest class.
        The OrderRequest.OrderId will default to OrderResponseErrorCode.UnableToFindOrder
        
        :param orderType: The order type to be submitted
        :param securityType: The symbol's SecurityType
        :param symbol: The symbol to be traded
        :param quantity: The number of units to be ordered
        :param stopPrice: The stop price for stop orders, non-stop orders this value is ignored
        :param limitPrice: The limit price for limit orders, non-limit orders this value is ignored
        :param triggerPrice: The trigger price for limit if touched orders, for non-limit if touched orders this value is ignored
        :param time: The time this request was created
        :param tag: A custom tag for this request
        :param properties: The order properties for this request
        :param groupOrderManager: The manager for this combo order
        """
        ...

    @overload
    def __init__(self, orderType: QuantConnect.Orders.OrderType, securityType: QuantConnect.SecurityType, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, stopPrice: float, limitPrice: float, time: typing.Union[datetime.datetime, datetime.date], tag: str, properties: QuantConnect.Interfaces.IOrderProperties = None, groupOrderManager: QuantConnect.Orders.GroupOrderManager = None) -> None:
        """
        Initializes a new instance of the SubmitOrderRequest class.
        The OrderRequest.OrderId will default to OrderResponseErrorCode.UnableToFindOrder
        
        :param orderType: The order type to be submitted
        :param securityType: The symbol's SecurityType
        :param symbol: The symbol to be traded
        :param quantity: The number of units to be ordered
        :param stopPrice: The stop price for stop orders, non-stop orders this value is ignored
        :param limitPrice: The limit price for limit orders, non-limit orders this value is ignored
        :param time: The time this request was created
        :param tag: A custom tag for this request
        :param properties: The order properties for this request
        :param groupOrderManager: The manager for this combo order
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class Order(System.Object, metaclass=abc.ABCMeta):
    """Order struct for placing new trade"""

    @property
    def Id(self) -> int:
        """Order ID."""
        ...

    @property
    def ContingentId(self) -> int:
        """Order id to process before processing this order."""
        ...

    @property
    def BrokerId(self) -> System.Collections.Generic.List[str]:
        """Brokerage Id for this order for when the brokerage splits orders into multiple pieces"""
        ...

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        """Symbol of the Asset"""
        ...

    @property
    def Price(self) -> float:
        """Price of the Order."""
        ...

    @property
    def PriceCurrency(self) -> str:
        """Currency for the order price"""
        ...

    @property
    def Time(self) -> datetime.datetime:
        """Gets the utc time the order was created."""
        ...

    @property
    def CreatedTime(self) -> datetime.datetime:
        """Gets the utc time this order was created. Alias for Time"""
        ...

    @property
    def LastFillTime(self) -> typing.Optional[datetime.datetime]:
        """Gets the utc time the last fill was received, or null if no fills have been received"""
        ...

    @property
    def LastUpdateTime(self) -> typing.Optional[datetime.datetime]:
        """Gets the utc time this order was last updated, or null if the order has not been updated."""
        ...

    @property
    def CanceledTime(self) -> typing.Optional[datetime.datetime]:
        """Gets the utc time this order was canceled, or null if the order was not canceled."""
        ...

    @property
    def Quantity(self) -> float:
        """Number of shares to execute."""
        ...

    @property
    @abc.abstractmethod
    def Type(self) -> int:
        """
        Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @property
    def Status(self) -> int:
        """
        Status of the Order
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderStatus enum.
        """
        ...

    @property
    def TimeInForce(self) -> QuantConnect.Orders.TimeInForce:
        """Order Time In Force"""
        ...

    @property
    def Tag(self) -> str:
        """Tag the order with some custom data"""
        ...

    @property
    def Properties(self) -> QuantConnect.Interfaces.IOrderProperties:
        """Additional properties of the order"""
        ...

    @property
    def SecurityType(self) -> int:
        """
        The symbol's security type
        
        This property contains the int value of a member of the QuantConnect.SecurityType enum.
        """
        ...

    @property
    def Direction(self) -> int:
        """
        Order Direction Property based off Quantity.
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderDirection enum.
        """
        ...

    @property
    def AbsoluteQuantity(self) -> float:
        """Get the absolute quantity for this order"""
        ...

    @property
    def Value(self) -> float:
        """
        Gets the executed value of this order. If the order has not yet filled,
        then this will return zero.
        """
        ...

    @property
    def OrderSubmissionData(self) -> QuantConnect.Orders.OrderSubmissionData:
        """Gets the price data at the time the order was submitted"""
        ...

    @property
    def IsMarketable(self) -> bool:
        """Returns true if the order is a marketable order."""
        ...

    @property
    def GroupOrderManager(self) -> QuantConnect.Orders.GroupOrderManager:
        """Manager for the orders in the group if this is a combo order"""
        ...

    @overload
    def __init__(self) -> None:
        """
        Added a default constructor for JSON Deserialization:
        
        This method is protected.
        """
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, time: typing.Union[datetime.datetime, datetime.date], groupOrderManager: QuantConnect.Orders.GroupOrderManager, tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New order constructor
        
        This method is protected.
        
        :param symbol: Symbol asset we're seeking to trade
        :param quantity: Quantity of the asset we're seeking to trade
        :param time: Time the order was placed
        :param groupOrderManager: Manager for the orders in the group if this is a combo order
        :param tag: User defined data tag for this order
        :param properties: The order properties for this order
        """
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, time: typing.Union[datetime.datetime, datetime.date], tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New order constructor
        
        This method is protected.
        
        :param symbol: Symbol asset we're seeking to trade
        :param quantity: Quantity of the asset we're seeking to trade
        :param time: Time the order was placed
        :param tag: User defined data tag for this order
        :param properties: The order properties for this order
        """
        ...

    def ApplyUpdateOrderRequest(self, request: QuantConnect.Orders.UpdateOrderRequest) -> None:
        """
        Modifies the state of this order to match the update request
        
        :param request: The request to update this order object
        """
        ...

    def Clone(self) -> QuantConnect.Orders.Order:
        """
        Creates a deep-copy clone of this order
        
        :returns: A copy of this order.
        """
        ...

    def CopyTo(self, order: QuantConnect.Orders.Order) -> None:
        """
        Copies base Order properties to the specified order
        
        This method is protected.
        
        :param order: The target of the copy
        """
        ...

    @staticmethod
    def CreateOrder(request: QuantConnect.Orders.SubmitOrderRequest) -> QuantConnect.Orders.Order:
        """
        Creates an Order to match the specified
        
        :param request: The SubmitOrderRequest to create an order for
        :returns: The Order that matches the request.
        """
        ...

    def CreatePositions(self, securities: QuantConnect.Securities.SecurityManager) -> System.Collections.Generic.IEnumerable[QuantConnect.Securities.Positions.IPosition]:
        """
        Creates an enumerable containing each position resulting from executing this order.
        
        :returns: An enumerable of positions matching the results of executing this order.
        """
        ...

    @staticmethod
    def FromSerialized(serializedOrder: QuantConnect.Orders.Serialization.SerializedOrder) -> QuantConnect.Orders.Order:
        """Creates a new Order instance from a SerializedOrder instance"""
        ...

    def GetValue(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the value of this order at the given market price in units of the account currency
        NOTE: Some order types derive value from other parameters, such as limit prices
        
        :param security: The security matching this order's symbol
        :returns: The value of this order given the current market price.
        """
        ...

    def GetValueImpl(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the order value in units of the security's quote currency for a single unit.
        A single unit here is a single share of stock, or a single barrel of oil, or the
        cost of a single share in an option contract.
        
        This method is protected.
        
        :param security: The security matching this order's symbol
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class OrderResponse(System.Object):
    """
    Represents a response to an OrderRequest. See OrderRequest.Response property for
    a specific request's response value
    """

    @property
    def OrderId(self) -> int:
        """Gets the order id"""
        ...

    @property
    def ErrorMessage(self) -> str:
        """
        Gets the error message if the ErrorCode does not equal OrderResponseErrorCode.None, otherwise
        gets string.Empty
        """
        ...

    @property
    def ErrorCode(self) -> int:
        """
        Gets the error code for this response.
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderResponseErrorCode enum.
        """
        ...

    @property
    def IsSuccess(self) -> bool:
        """
        Gets true if this response represents a successful request, false otherwise
        If this is an unprocessed response, IsSuccess will return false.
        """
        ...

    @property
    def IsError(self) -> bool:
        """Gets true if this response represents an error, false otherwise"""
        ...

    @property
    def IsProcessed(self) -> bool:
        """Gets true if this response has been processed, false otherwise"""
        ...

    Unprocessed: QuantConnect.Orders.OrderResponse = ...

    @staticmethod
    def Error(request: QuantConnect.Orders.OrderRequest, errorCode: QuantConnect.Orders.OrderResponseErrorCode, errorMessage: str) -> QuantConnect.Orders.OrderResponse:
        """Helper method to create an error response from a request"""
        ...

    @staticmethod
    def InvalidNewStatus(request: QuantConnect.Orders.OrderRequest, order: QuantConnect.Orders.Order) -> QuantConnect.Orders.OrderResponse:
        """Helper method to create an error response due to the "New" order status"""
        ...

    @staticmethod
    def InvalidStatus(request: QuantConnect.Orders.OrderRequest, order: QuantConnect.Orders.Order) -> QuantConnect.Orders.OrderResponse:
        """Helper method to create an error response due to an invalid order status"""
        ...

    @staticmethod
    def MissingSecurity(request: QuantConnect.Orders.SubmitOrderRequest) -> QuantConnect.Orders.OrderResponse:
        """Helper method to create an error response due to a missing security"""
        ...

    @staticmethod
    def Success(request: QuantConnect.Orders.OrderRequest) -> QuantConnect.Orders.OrderResponse:
        """Helper method to create a successful response from a request"""
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...

    @staticmethod
    def UnableToFindOrder(request: QuantConnect.Orders.OrderRequest) -> QuantConnect.Orders.OrderResponse:
        """Helper method to create an error response due to a bad order id"""
        ...

    @staticmethod
    def WarmingUp(request: QuantConnect.Orders.OrderRequest) -> QuantConnect.Orders.OrderResponse:
        """Helper method to create an error response due to algorithm still in warmup mode"""
        ...

    @staticmethod
    def ZeroQuantity(request: QuantConnect.Orders.OrderRequest) -> QuantConnect.Orders.OrderResponse:
        """Helper method to create an error response due to a zero order quantity"""
        ...


class MarketOrder(QuantConnect.Orders.Order):
    """Market order type definition"""

    @property
    def Type(self) -> int:
        """
        Market Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Added a default constructor for JSON Deserialization:"""
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, time: typing.Union[datetime.datetime, datetime.date], price: float, tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New market order constructor
        
        :param symbol: Symbol asset we're seeking to trade
        :param quantity: Quantity of the asset we're seeking to trade
        :param time: Time the order was placed
        :param price: Price of the order
        :param tag: User defined data tag for this order
        :param properties: The order properties for this order
        """
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, time: typing.Union[datetime.datetime, datetime.date], tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New market order constructor
        
        :param symbol: Symbol asset we're seeking to trade
        :param quantity: Quantity of the asset we're seeking to trade
        :param time: Time the order was placed
        :param tag: User defined data tag for this order
        :param properties: The order properties for this order
        """
        ...

    def Clone(self) -> QuantConnect.Orders.Order:
        """
        Creates a deep-copy clone of this order
        
        :returns: A copy of this order.
        """
        ...

    def GetValueImpl(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the order value in units of the security's quote currency
        
        This method is protected.
        
        :param security: The security matching this order's symbol
        """
        ...


class MarketOnCloseOrder(QuantConnect.Orders.Order):
    """Market on close order type - submits a market order on exchange close"""

    DefaultSubmissionTimeBuffer: datetime.timedelta = ...
    """
    Gets the default interval before market close that an MOC order may be submitted.
    For example, US equity exchanges typically require MOC orders to be placed no later
    than 15 minutes before market close, which yields a nominal time of 3:45PM.
    This buffer value takes into account the 15 minutes and adds an additional 30 seconds
    to account for other potential delays, such as LEAN order processing and placement of
    the order to the exchange.
    """

    SubmissionTimeBuffer: datetime.timedelta = ...
    """The interval before market close that an MOC order may be submitted."""

    @property
    def Type(self) -> int:
        """
        MarketOnClose Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Intiializes a new instance of the MarketOnCloseOrder class."""
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, time: typing.Union[datetime.datetime, datetime.date], tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        Intiializes a new instance of the MarketOnCloseOrder class.
        
        :param symbol: The security's symbol being ordered
        :param quantity: The number of units to order
        :param time: The current time
        :param tag: A user defined tag for the order
        :param properties: The order properties for this order
        """
        ...

    def Clone(self) -> QuantConnect.Orders.Order:
        """
        Creates a deep-copy clone of this order
        
        :returns: A copy of this order.
        """
        ...

    def GetValueImpl(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the order value in units of the security's quote currency
        
        This method is protected.
        
        :param security: The security matching this order's symbol
        """
        ...


class OrderJsonConverter(JsonConverter):
    """Provides an implementation of JsonConverter that can deserialize Orders"""

    @property
    def CanWrite(self) -> bool:
        """Gets a value indicating whether this Newtonsoft.Json.JsonConverter can write JSON."""
        ...

    def CanConvert(self, objectType: typing.Type) -> bool:
        """
        Determines whether this instance can convert the specified object type.
        
        :param objectType: Type of the object.
        :returns: true if this instance can convert the specified object type; otherwise, false.
        """
        ...

    @staticmethod
    def CreateOrderFromJObject(jObject: typing.Any) -> QuantConnect.Orders.Order:
        """
        Create an order from a simple JObject
        
        :returns: Order Object.
        """
        ...

    def ReadJson(self, reader: typing.Any, objectType: typing.Type, existingValue: typing.Any, serializer: typing.Any) -> System.Object:
        """
        Reads the JSON representation of the object.
        
        :param reader: The Newtonsoft.Json.JsonReader to read from.
        :param objectType: Type of the object.
        :param existingValue: The existing value of object being read.
        :param serializer: The calling serializer.
        :returns: The object value.
        """
        ...

    def WriteJson(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """
        Writes the JSON representation of the object.
        
        :param writer: The Newtonsoft.Json.JsonWriter to write to.
        :param value: The value.
        :param serializer: The calling serializer.
        """
        ...


class OrderProperties(System.Object, QuantConnect.Interfaces.IOrderProperties):
    """Contains additional properties and settings for an order"""

    @property
    def TimeInForce(self) -> QuantConnect.Orders.TimeInForce:
        """Defines the length of time over which an order will continue working before it is cancelled"""
        ...

    @property
    def Exchange(self) -> QuantConnect.Exchange:
        """Defines the exchange name for a particular market"""
        ...

    @overload
    def __init__(self) -> None:
        """Initializes a new instance of the OrderProperties class"""
        ...

    @overload
    def __init__(self, exchange: QuantConnect.Exchange) -> None:
        """
        Initializes a new instance of the OrderProperties class, with exchange param
        Exchange name for market
        
        :param exchange: Exchange name for market
        """
        ...

    def Clone(self) -> QuantConnect.Interfaces.IOrderProperties:
        """Returns a new instance clone of this object"""
        ...


class BybitOrderProperties(QuantConnect.Orders.OrderProperties):
    """This class has no documentation."""

    @property
    def PostOnly(self) -> bool:
        """
        This flag will ensure the order executes only as a maker (no fee) order.
        If part of the order results in taking liquidity rather than providing,
        it will be rejected and no part of the order will execute.
        Note: this flag is only applied to Limit orders.
        """
        ...

    @property
    def ReduceOnly(self) -> typing.Optional[bool]:
        """This flag will ensure your position can only reduce in size if the order is triggered."""
        ...


class RBIOrderProperties(QuantConnect.Orders.OrderProperties):
    """RBI order properties"""


class StopMarketOrder(QuantConnect.Orders.Order):
    """Stop Market Order Type Definition"""

    @property
    def StopPrice(self) -> float:
        """Stop price for this stop market order."""
        ...

    @property
    def Type(self) -> int:
        """
        StopMarket Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Default constructor for JSON Deserialization:"""
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, stopPrice: float, time: typing.Union[datetime.datetime, datetime.date], tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New Stop Market Order constructor -
        
        :param symbol: Symbol asset we're seeking to trade
        :param quantity: Quantity of the asset we're seeking to trade
        :param stopPrice: Price the order should be filled at if a limit order
        :param time: Time the order was placed
        :param tag: User defined data tag for this order
        :param properties: The order properties for this order
        """
        ...

    def ApplyUpdateOrderRequest(self, request: QuantConnect.Orders.UpdateOrderRequest) -> None:
        """
        Modifies the state of this order to match the update request
        
        :param request: The request to update this order object
        """
        ...

    def Clone(self) -> QuantConnect.Orders.Order:
        """
        Creates a deep-copy clone of this order
        
        :returns: A copy of this order.
        """
        ...

    def GetValueImpl(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the order value in units of the security's quote currency
        
        This method is protected.
        
        :param security: The security matching this order's symbol
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class OrderDirection(System.Enum):
    """Direction of the order"""

    Buy = 0
    """Buy Order (0)"""

    Sell = 1
    """Sell Order (1)"""

    Hold = 2
    """Default Value - No Order Direction (2)"""


class TrailingStopOrder(QuantConnect.Orders.StopMarketOrder):
    """Trailing Stop Order Type Definition"""

    @property
    def TrailingAmount(self) -> float:
        """Trailing amount for this trailing stop order"""
        ...

    @property
    def TrailingAsPercentage(self) -> bool:
        """Determines whether the TrailingAmount is a percentage or an absolute currency value"""
        ...

    @property
    def Type(self) -> int:
        """
        StopLimit Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Default constructor for JSON Deserialization:"""
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, stopPrice: float, trailingAmount: float, trailingAsPercentage: bool, time: typing.Union[datetime.datetime, datetime.date], tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New Trailing Stop Market Order constructor
        
        :param symbol: Symbol asset being traded
        :param quantity: Quantity of the asset to be traded
        :param stopPrice: Initial stop price at which the order should be triggered
        :param trailingAmount: The trailing amount to be used to update the stop price
        :param trailingAsPercentage: Whether the  is a percentage or an absolute currency value
        :param time: Time the order was placed
        :param tag: User defined data tag for this order
        :param properties: The properties for this order
        """
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, trailingAmount: float, trailingAsPercentage: bool, time: typing.Union[datetime.datetime, datetime.date], tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New Trailing Stop Market Order constructor.
        It creates a new Trailing Stop Market Order with an initial stop price calculated by subtracting (for a sell) or adding (for a buy) the
        trailing amount to the current market price.
        
        :param symbol: Symbol asset being traded
        :param quantity: Quantity of the asset to be traded
        :param trailingAmount: The trailing amount to be used to update the stop price
        :param trailingAsPercentage: Whether the  is a percentage or an absolute currency value
        :param time: Time the order was placed
        :param tag: User defined data tag for this order
        :param properties: The properties for this order
        """
        ...

    def ApplyUpdateOrderRequest(self, request: QuantConnect.Orders.UpdateOrderRequest) -> None:
        """
        Modifies the state of this order to match the update request
        
        :param request: The request to update this order object
        """
        ...

    @staticmethod
    def CalculateStopPrice(currentMarketPrice: float, trailingAmount: float, trailingAsPercentage: bool, direction: QuantConnect.Orders.OrderDirection) -> float:
        """
        Calculates the stop price for a trailing stop order given the current market price
        
        :param currentMarketPrice: The current market price
        :param trailingAmount: The trailing amount to be used to update the stop price
        :param trailingAsPercentage: Whether the  is a percentage or an absolute currency value
        :param direction: The order direction
        :returns: The stop price for the order given the current market price.
        """
        ...

    def Clone(self) -> QuantConnect.Orders.Order:
        """
        Creates a deep-copy clone of this order
        
        :returns: A copy of this order.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...

    @staticmethod
    def TryUpdateStopPrice(currentMarketPrice: float, currentStopPrice: float, trailingAmount: float, trailingAsPercentage: bool, direction: QuantConnect.Orders.OrderDirection, updatedStopPrice: typing.Optional[float]) -> typing.Union[bool, float]:
        """
        Tries to update the stop price for a trailing stop order given the current market price
        
        :param currentMarketPrice: The current market price
        :param currentStopPrice: The current trailing stop order stop price
        :param trailingAmount: The trailing amount to be used to update the stop price
        :param trailingAsPercentage: Whether the  is a percentage or an absolute currency value
        :param direction: The order direction
        :param updatedStopPrice: The updated stop price
        :returns: Whether the stop price was updated. This only happens when the distance between the current stop price and the current market price is greater than the trailing amount, which will happen when the market price raises/falls for sell/buy orders respectively.
        """
        ...


class StopLimitOrder(QuantConnect.Orders.Order):
    """Stop Market Order Type Definition"""

    @property
    def StopPrice(self) -> float:
        """Stop price for this stop market order."""
        ...

    @property
    def StopTriggered(self) -> bool:
        """Signal showing the "StopLimitOrder" has been converted into a Limit Order"""
        ...

    @property
    def LimitPrice(self) -> float:
        """Limit price for the stop limit order"""
        ...

    @property
    def Type(self) -> int:
        """
        StopLimit Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Default constructor for JSON Deserialization:"""
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, stopPrice: float, limitPrice: float, time: typing.Union[datetime.datetime, datetime.date], tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New Stop Market Order constructor -
        
        :param symbol: Symbol asset we're seeking to trade
        :param quantity: Quantity of the asset we're seeking to trade
        :param stopPrice: Price the order should be filled at if a limit order
        :param limitPrice: Maximum price to fill the order
        :param time: Time the order was placed
        :param tag: User defined data tag for this order
        :param properties: The order properties for this order
        """
        ...

    def ApplyUpdateOrderRequest(self, request: QuantConnect.Orders.UpdateOrderRequest) -> None:
        """
        Modifies the state of this order to match the update request
        
        :param request: The request to update this order object
        """
        ...

    def Clone(self) -> QuantConnect.Orders.Order:
        """
        Creates a deep-copy clone of this order
        
        :returns: A copy of this order.
        """
        ...

    def GetValueImpl(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the order value in units of the security's quote currency
        
        This method is protected.
        
        :param security: The security matching this order's symbol
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class AtreyuOrderProperties(System.Object, QuantConnect.Interfaces.IOrderProperties):
    """Contains additional properties and settings for an order submitted to Atreyu brokerage"""

    @property
    def TimeInForce(self) -> QuantConnect.Orders.TimeInForce:
        """Defines the length of time over which an order will continue working before it is cancelled"""
        ...

    @property
    def PostOnly(self) -> bool:
        """This flag will ensure the order add liquidity only"""
        ...

    def __init__(self) -> None:
        """Creates a new instance and sets TimeInForce to Day"""
        ...

    def Clone(self) -> QuantConnect.Interfaces.IOrderProperties:
        """Returns a new instance clone of this object"""
        ...


class TerminalLinkOrderProperties(QuantConnect.Orders.OrderProperties):
    """The terminal link order properties"""

    class StrategyParameters(System.Object):
        """Models an EMSX order strategy parameter"""

        @property
        def Name(self) -> str:
            """The strategy name"""
            ...

        @property
        def Fields(self) -> System.Collections.Generic.List[QuantConnect.Orders.TerminalLinkOrderProperties.StrategyField]:
            """The strategy fields"""
            ...

        def __init__(self, name: str, fields: System.Collections.Generic.List[QuantConnect.Orders.TerminalLinkOrderProperties.StrategyField]) -> None:
            """
            Creates a new TerminalLink order strategy instance
            
            :param name: The strategy name
            :param fields: The strategy fields
            """
            ...

    class StrategyField(System.Object):
        """Models an EMSX order strategy field"""

        @property
        def Value(self) -> str:
            """The strategy field value"""
            ...

        @property
        def HasValue(self) -> bool:
            """Whether the strategy field carries a value"""
            ...

        @overload
        def __init__(self, value: str) -> None:
            """
            Creates a new TerminalLink order strategy field carrying a value.
            
            :param value: The strategy field value
            """
            ...

        @overload
        def __init__(self) -> None:
            """Creates a new TerminalLink order strategy field without a value."""
            ...

    @property
    def Notes(self) -> str:
        """The EMSX Instructions is the free form instructions that may be sent to the broker"""
        ...

    @property
    def HandlingInstruction(self) -> str:
        """
        The EMSX Handling Instruction is the instructions for handling the order or route.The values can be
        preconfigured or a value customized by the broker.
        """
        ...

    @property
    def CustomNotes1(self) -> str:
        """Custom user order notes 1"""
        ...

    @property
    def CustomNotes2(self) -> str:
        """Custom user order notes 2"""
        ...

    @property
    def CustomNotes3(self) -> str:
        """Custom user order notes 3"""
        ...

    @property
    def CustomNotes4(self) -> str:
        """Custom user order notes 4"""
        ...

    @property
    def CustomNotes5(self) -> str:
        """Custom user order notes 5"""
        ...

    @property
    def Account(self) -> str:
        """The EMSX account"""
        ...

    @property
    def Broker(self) -> str:
        """The EMSX broker code"""
        ...

    @property
    def Strategy(self) -> QuantConnect.Orders.TerminalLinkOrderProperties.StrategyParameters:
        """
        The EMSX order strategy details.
        Strategy parameters must be appended in the correct order as expected by EMSX.
        """
        ...


class TDAmeritradeOrderProperties(QuantConnect.Orders.OrderProperties):
    """TDAmeritrade order properties"""


class KrakenOrderProperties(QuantConnect.Orders.OrderProperties):
    """Kraken order properties"""

    @property
    def PostOnly(self) -> bool:
        """Post-only order (available when ordertype = limit)"""
        ...

    @property
    def FeeInBase(self) -> bool:
        """If true or by default when selling, fees will be charged in base currency. If false will be ignored. Mutually exclusive with FeeInQuote."""
        ...

    @property
    def FeeInQuote(self) -> bool:
        """If true or by default when buying, fees will be charged in quote currency. If false will be ignored. Mutually exclusive with FeeInBase."""
        ...

    @property
    def NoMarketPriceProtection(self) -> bool:
        """https://support.kraken.com/hc/en-us/articles/201648183-Market-Price-Protection"""
        ...

    @property
    def ConditionalOrder(self) -> QuantConnect.Orders.Order:
        """Conditional close orders are triggered by execution of the primary order in the same quantity and opposite direction. Ordertypes can be the same with primary order."""
        ...


class OrderSizing(System.Object):
    """Provides methods for computing a maximum order size."""

    @staticmethod
    def AdjustByLotSize(security: QuantConnect.Securities.Security, quantity: float) -> float:
        """
        Adjusts the provided order quantity to respect the securities lot size.
        If the quantity is missing 1M part of the lot size it will be rounded up
        since we suppose it's due to floating point error, this is required to avoid diff
        between Py and C#
        
        :param security: The security instance
        :param quantity: The desired quantity to adjust, can be signed
        :returns: The signed adjusted quantity.
        """
        ...

    @staticmethod
    def GetOrderSizeForMaximumValue(security: QuantConnect.Securities.Security, maximumOrderValueInAccountCurrency: float, desiredOrderSize: float) -> float:
        """
        Adjust the provided order size to respect the maximum total order value
        
        :param security: The security object
        :param maximumOrderValueInAccountCurrency: The maximum order value in units of the account currency
        :param desiredOrderSize: The desired order size to adjust
        :returns: The signed adjusted order size.
        """
        ...

    @staticmethod
    def GetOrderSizeForPercentVolume(security: QuantConnect.Securities.Security, maximumPercentCurrentVolume: float, desiredOrderSize: float) -> float:
        """
        Adjust the provided order size to respect maximum order size based on a percentage of current volume.
        
        :param security: The security object
        :param maximumPercentCurrentVolume: The maximum percentage of the current bar's volume
        :param desiredOrderSize: The desired order size to adjust
        :returns: The signed adjusted order size.
        """
        ...

    @staticmethod
    @overload
    def GetUnorderedQuantity(algorithm: QuantConnect.Interfaces.IAlgorithm, target: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget) -> float:
        """
        Gets the remaining quantity to be ordered to reach the specified target quantity.
        
        :param algorithm: The algorithm instance
        :param target: The portfolio target
        :returns: The signed remaining quantity to be ordered.
        """
        ...

    @staticmethod
    @overload
    def GetUnorderedQuantity(algorithm: QuantConnect.Interfaces.IAlgorithm, target: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the remaining quantity to be ordered to reach the specified target quantity.
        
        :param algorithm: The algorithm instance
        :param target: The portfolio target
        :param security: The target security
        :returns: The signed remaining quantity to be ordered.
        """
        ...


class CancelOrderRequest(QuantConnect.Orders.OrderRequest):
    """Defines a request to cancel an order"""

    @property
    def OrderRequestType(self) -> int:
        """
        Gets Orders.OrderRequestType.Cancel
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderRequestType enum.
        """
        ...

    def __init__(self, time: typing.Union[datetime.datetime, datetime.date], orderId: int, tag: str) -> None:
        """
        Initializes a new instance of the CancelOrderRequest class
        
        :param time: The time this cancelation was requested
        :param orderId: The order id to be canceled
        :param tag: A new tag for the order
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class OrderField(System.Enum):
    """Specifies an order field that does not apply to all order types"""

    LimitPrice = 0
    """The limit price for a LimitOrder, StopLimitOrder or LimitIfTouchedOrder (0)"""

    StopPrice = 1
    """The stop price for stop orders (StopMarketOrder, StopLimitOrder) (1)"""

    TriggerPrice = 2
    """The trigger price for a LimitIfTouchedOrder (2)"""

    TrailingAmount = 3
    """The trailing amount for a TrailingStopOrder (3)"""

    TrailingAsPercentage = 4
    """Whether the trailing amount for a TrailingStopOrder is a percentage or an absolute currency value (4)"""


class OrderStatus(System.Enum):
    """Fill status of the order class."""

    New = 0
    """New order pre-submission to the order processor (0)"""

    Submitted = 1
    """Order submitted to the market (1)"""

    PartiallyFilled = 2
    """Partially filled, In Market Order (2)"""

    Filled = 3
    """Completed, Filled, In Market Order (3)"""

    Canceled = 5
    """Order cancelled before it was filled (5)"""

    # Cannot convert to Python: None = 6
    """No Order State Yet (6)"""

    Invalid = 7
    """Order invalidated before it hit the market (e.g. insufficient capital) (7)"""

    CancelPending = 8
    """Order waiting for confirmation of cancellation (6)"""

    UpdateSubmitted = 9
    """Order update submitted to the market (9)"""


class OrderEvent(System.Object):
    """Order Event - Messaging class signifying a change in an order state and record the change in the user's algorithm portfolio"""

    @property
    def OrderId(self) -> int:
        """Id of the order this event comes from."""
        ...

    @property
    def Id(self) -> int:
        """The unique order event id for each order"""
        ...

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        """Easy access to the order symbol associated with this event."""
        ...

    @property
    def UtcTime(self) -> datetime.datetime:
        """The date and time of this event (UTC)."""
        ...

    @property
    def Status(self) -> int:
        """
        Status message of the order.
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderStatus enum.
        """
        ...

    @property
    def OrderFee(self) -> QuantConnect.Orders.Fees.OrderFee:
        """The fee associated with the order"""
        ...

    @property
    def FillPrice(self) -> float:
        """Fill price information about the order"""
        ...

    @property
    def FillPriceCurrency(self) -> str:
        """Currency for the fill price"""
        ...

    @property
    def FillQuantity(self) -> float:
        """Number of shares of the order that was filled in this event."""
        ...

    @property
    def AbsoluteFillQuantity(self) -> float:
        """Public Property Absolute Getter of Quantity -Filled"""
        ...

    @property
    def Direction(self) -> int:
        """
        Order direction.
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderDirection enum.
        """
        ...

    @property
    def Message(self) -> str:
        """Any message from the exchange."""
        ...

    @property
    def IsAssignment(self) -> bool:
        """True if the order event is an assignment"""
        ...

    @property
    def StopPrice(self) -> typing.Optional[float]:
        """The current stop price"""
        ...

    @property
    def TriggerPrice(self) -> typing.Optional[float]:
        """The current trigger price"""
        ...

    @property
    def LimitPrice(self) -> typing.Optional[float]:
        """The current limit price"""
        ...

    @property
    def Quantity(self) -> float:
        """The current order quantity"""
        ...

    @property
    def IsInTheMoney(self) -> bool:
        """True if the order event's option is In-The-Money (ITM)"""
        ...

    @property
    def TrailingAmount(self) -> typing.Optional[float]:
        """The trailing stop amount"""
        ...

    @property
    def TrailingAsPercentage(self) -> typing.Optional[bool]:
        """Whether the TrailingAmount is a percentage or an absolute currency value"""
        ...

    @property
    def Ticket(self) -> QuantConnect.Orders.OrderTicket:
        """The order ticket associated to the order"""
        ...

    @overload
    def __init__(self) -> None:
        """Order Event empty constructor required for json converter"""
        ...

    @overload
    def __init__(self, orderId: int, symbol: typing.Union[QuantConnect.Symbol, str], utcTime: typing.Union[datetime.datetime, datetime.date], status: QuantConnect.Orders.OrderStatus, direction: QuantConnect.Orders.OrderDirection, fillPrice: float, fillQuantity: float, orderFee: QuantConnect.Orders.Fees.OrderFee, message: str = ...) -> None:
        """
        Order Event Constructor.
        
        :param orderId: Id of the parent order
        :param symbol: Asset Symbol
        :param utcTime: Date/time of this event
        :param status: Status of the order
        :param direction: The direction of the order this event belongs to
        :param fillPrice: Fill price information if applicable.
        :param fillQuantity: Fill quantity
        :param orderFee: The order fee
        :param message: Message from the exchange
        """
        ...

    @overload
    def __init__(self, order: QuantConnect.Orders.Order, utcTime: typing.Union[datetime.datetime, datetime.date], orderFee: QuantConnect.Orders.Fees.OrderFee, message: str = ...) -> None:
        """
        Helper Constructor using Order to Initialize.
        
        :param order: Order for this order status
        :param utcTime: Date/time of this event
        :param orderFee: The order fee
        :param message: Message from exchange or QC.
        """
        ...

    def Clone(self) -> QuantConnect.Orders.OrderEvent:
        """
        Returns a clone of the current object.
        
        :returns: The new clone object.
        """
        ...

    @staticmethod
    def FromSerialized(serializedOrderEvent: QuantConnect.Orders.Serialization.SerializedOrderEvent) -> QuantConnect.Orders.OrderEvent:
        """Creates a new instance based on the provided serialized order event"""
        ...

    def ShortToString(self) -> str:
        """Returns a short string that represents the current object."""
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class OrderTicket(System.Object):
    """
    Provides a single reference to an order for the algorithm to maintain. As the order gets
    updated this ticket will also get updated
    """

    @property
    def OrderId(self) -> int:
        """Gets the order id of this ticket"""
        ...

    @property
    def Status(self) -> int:
        """
        Gets the current status of this order ticket
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderStatus enum.
        """
        ...

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        """Gets the symbol being ordered"""
        ...

    @property
    def SecurityType(self) -> int:
        """
        Gets the Symbol's SecurityType
        
        This property contains the int value of a member of the QuantConnect.SecurityType enum.
        """
        ...

    @property
    def Quantity(self) -> float:
        """Gets the number of units ordered"""
        ...

    @property
    def AverageFillPrice(self) -> float:
        """
        Gets the average fill price for this ticket. If no fills have been processed
        then this will return a value of zero.
        """
        ...

    @property
    def QuantityFilled(self) -> float:
        """
        Gets the total qantity filled for this ticket. If no fills have been processed
        then this will return a value of zero.
        """
        ...

    @property
    def Time(self) -> datetime.datetime:
        """Gets the time this order was last updated"""
        ...

    @property
    def OrderType(self) -> int:
        """
        Gets the type of order
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @property
    def Tag(self) -> str:
        """Gets the order's current tag"""
        ...

    @property
    def SubmitRequest(self) -> QuantConnect.Orders.SubmitOrderRequest:
        """Gets the SubmitOrderRequest that initiated this order"""
        ...

    @property
    def UpdateRequests(self) -> System.Collections.Generic.IReadOnlyList[QuantConnect.Orders.UpdateOrderRequest]:
        """
        Gets a list of UpdateOrderRequest containing an item for each
        UpdateOrderRequest that was sent for this order id
        """
        ...

    @property
    def CancelRequest(self) -> QuantConnect.Orders.CancelOrderRequest:
        """
        Gets the CancelOrderRequest if this order was canceled. If this order
        was not canceled, this will return null
        """
        ...

    @property
    def OrderEvents(self) -> System.Collections.Generic.IReadOnlyList[QuantConnect.Orders.OrderEvent]:
        """Gets a list of all order events for this ticket"""
        ...

    @property
    def OrderClosed(self) -> System.Threading.WaitHandle:
        """Gets a wait handle that can be used to wait until this order has filled"""
        ...

    @property
    def HasOrder(self) -> bool:
        """Returns true if the order has been set for this ticket"""
        ...

    @property
    def OrderSet(self) -> System.Threading.WaitHandle:
        """Gets a wait handle that can be used to wait until the order has been set"""
        ...

    def __init__(self, transactionManager: QuantConnect.Securities.SecurityTransactionManager, submitRequest: QuantConnect.Orders.SubmitOrderRequest) -> None:
        """
        Initializes a new instance of the OrderTicket class
        
        :param transactionManager: The transaction manager used for submitting updates and cancels for this ticket
        :param submitRequest: The order request that initiated this order ticket
        """
        ...

    def Cancel(self, tag: str = None) -> QuantConnect.Orders.OrderResponse:
        """Submits a new request to cancel this order"""
        ...

    @overload
    def Get(self, field: QuantConnect.Orders.OrderField) -> float:
        """
        Gets the specified field from the ticket
        
        :param field: The order field to get
        :returns: The value of the field.
        """
        ...

    @overload
    def Get(self, field: QuantConnect.Orders.OrderField) -> QuantConnect_Orders_OrderTicket_Get_T:
        """
        Gets the specified field from the ticket and tries to convert it to the specified type
        
        :param field: The order field to get
        :returns: The value of the field.
        """
        ...

    def GetMostRecentOrderRequest(self) -> QuantConnect.Orders.OrderRequest:
        """
        Gets the most recent OrderRequest for this ticket
        
        :returns: The most recent OrderRequest for this ticket.
        """
        ...

    def GetMostRecentOrderResponse(self) -> QuantConnect.Orders.OrderResponse:
        """
        Gets the most recent OrderResponse for this ticket
        
        :returns: The most recent OrderResponse for this ticket.
        """
        ...

    @staticmethod
    def InvalidCancelOrderId(transactionManager: QuantConnect.Securities.SecurityTransactionManager, request: QuantConnect.Orders.CancelOrderRequest) -> QuantConnect.Orders.OrderTicket:
        """Creates a new OrderTicket that represents trying to cancel an order for which no ticket exists"""
        ...

    @staticmethod
    def InvalidSubmitRequest(transactionManager: QuantConnect.Securities.SecurityTransactionManager, request: QuantConnect.Orders.SubmitOrderRequest, response: QuantConnect.Orders.OrderResponse) -> QuantConnect.Orders.OrderTicket:
        """Creates a new OrderTicket that represents trying to submit a new order that had errors embodied in the"""
        ...

    @staticmethod
    def InvalidUpdateOrderId(transactionManager: QuantConnect.Securities.SecurityTransactionManager, request: QuantConnect.Orders.UpdateOrderRequest) -> QuantConnect.Orders.OrderTicket:
        """Creates a new OrderTicket that represents trying to update an order for which no ticket exists"""
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...

    def Update(self, fields: QuantConnect.Orders.UpdateOrderFields) -> QuantConnect.Orders.OrderResponse:
        """
        Submits an UpdateOrderRequest with the SecurityTransactionManager to update
        the ticket with data specified in
        
        :param fields: Defines what properties of the order should be updated
        :returns: The OrderResponse from updating the order.
        """
        ...

    def UpdateLimitPrice(self, limitPrice: float, tag: str = None) -> QuantConnect.Orders.OrderResponse:
        """
        Submits an UpdateOrderRequest with the SecurityTransactionManager to update
        the ticker with limit price specified in  and with tag specified in
        
        :param limitPrice: The new limit price for this order ticket
        :param tag: The new tag for this order ticket
        :returns: OrderResponse from updating the order.
        """
        ...

    def UpdateQuantity(self, quantity: float, tag: str = None) -> QuantConnect.Orders.OrderResponse:
        """
        Submits an UpdateOrderRequest with the SecurityTransactionManager to update
        the ticket with quantity specified in  and with tag specified in
        
        :param quantity: The new quantity for this order ticket
        :param tag: The new tag for this order ticket
        :returns: OrderResponse from updating the order.
        """
        ...

    def UpdateStopPrice(self, stopPrice: float, tag: str = None) -> QuantConnect.Orders.OrderResponse:
        """
        Submits an UpdateOrderRequest with the SecurityTransactionManager to update
        the ticker with stop price specified in  and with tag specified in
        
        :param stopPrice: The new stop price  for this order ticket
        :param tag: The new tag for this order ticket
        :returns: OrderResponse from updating the order.
        """
        ...

    def UpdateStopTrailingAmount(self, trailingAmount: float, tag: str = None) -> QuantConnect.Orders.OrderResponse:
        """
        Submits an UpdateOrderRequest with the SecurityTransactionManager to update
        the ticker with stop trailing amount specified in  and with tag specified in
        
        :param trailingAmount: The new trailing amount for this order ticket
        :param tag: The new tag for this order ticket
        :returns: OrderResponse from updating the order.
        """
        ...

    def UpdateTag(self, tag: str) -> QuantConnect.Orders.OrderResponse:
        """
        Submits an UpdateOrderRequest with the SecurityTransactionManager to update
        the ticket with tag specified in
        
        :param tag: The new tag for this order ticket
        :returns: OrderResponse from updating the order.
        """
        ...

    def UpdateTriggerPrice(self, triggerPrice: float, tag: str = None) -> QuantConnect.Orders.OrderResponse:
        """
        Submits an UpdateOrderRequest with the SecurityTransactionManager to update
        the ticker with trigger price specified in  and with tag specified in
        
        :param triggerPrice: The new price which, when touched, will trigger the setting of a limit order.
        :param tag: The new tag for this order ticket
        :returns: OrderResponse from updating the order.
        """
        ...


class InteractiveBrokersOrderProperties(QuantConnect.Orders.OrderProperties):
    """Contains additional properties and settings for an order submitted to Interactive Brokers"""

    @property
    def Account(self) -> str:
        """The linked account for which to submit the order (only used by Financial Advisors)"""
        ...

    @property
    def FaGroup(self) -> str:
        """The account group for the order (only used by Financial Advisors)"""
        ...

    @property
    def FaMethod(self) -> str:
        """
        The allocation method for the account group order (only used by Financial Advisors)
        Supported allocation methods are: EqualQuantity, NetLiq, AvailableEquity, PctChange
        """
        ...

    @property
    def FaPercentage(self) -> int:
        """The percentage for the percent change method (only used by Financial Advisors)"""
        ...

    @property
    def FaProfile(self) -> str:
        """The allocation profile to be used for the order (only used by Financial Advisors)"""
        ...

    @property
    def OutsideRegularTradingHours(self) -> bool:
        """If set to true, allows orders to also trigger or fill outside of regular trading hours."""
        ...

    def Clone(self) -> QuantConnect.Interfaces.IOrderProperties:
        """Returns a new instance clone of this object"""
        ...


class OptionExerciseOrder(QuantConnect.Orders.Order):
    """Option exercise order type definition"""

    @property
    def Type(self) -> int:
        """
        Option Exercise Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Added a default constructor for JSON Deserialization:"""
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, time: typing.Union[datetime.datetime, datetime.date], tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New option exercise order constructor. We model option exercising as an underlying asset long/short order with strike equal to limit price.
        This means that by exercising a call we get into long asset position, by exercising a put we get into short asset position.
        
        :param symbol: Option symbol we're seeking to exercise
        :param quantity: Quantity of the option we're seeking to exercise. Must be a positive value.
        :param time: Time the order was placed
        :param tag: User defined data tag for this order
        :param properties: The order properties for this order
        """
        ...

    def Clone(self) -> QuantConnect.Orders.Order:
        """
        Creates a deep-copy clone of this order
        
        :returns: A copy of this order.
        """
        ...

    def GetValueImpl(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the order value in option contracts quoted in options's currency
        
        This method is protected.
        
        :param security: The security matching this order's symbol
        """
        ...


class ComboMarketOrder(QuantConnect.Orders.MarketOrder):
    """Combo market order type"""

    @property
    def Type(self) -> int:
        """
        Combo Market Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Added a default constructor for JSON Deserialization:"""
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, time: typing.Union[datetime.datetime, datetime.date], groupOrderManager: QuantConnect.Orders.GroupOrderManager, tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New market order constructor
        
        :param symbol: Symbol asset we're seeking to trade
        :param quantity: Quantity of the asset we're seeking to trade
        :param time: Time the order was placed
        :param groupOrderManager: Manager for the orders in the group
        :param tag: User defined data tag for this order
        :param properties: The order properties for this order
        """
        ...

    def Clone(self) -> QuantConnect.Orders.Order:
        """
        Creates a deep-copy clone of this order
        
        :returns: A copy of this order.
        """
        ...


class FixOrderProperites(QuantConnect.Orders.OrderProperties):
    """FIX (Financial Information Exchange) order properties"""

    @property
    def HandleInstruction(self) -> typing.Optional[str]:
        """Instruction for order handling on Broker floor"""
        ...

    @property
    def Notes(self) -> str:
        """Free format text string"""
        ...

    AutomatedExecutionOrderPrivate: str = ...
    """Automated execution order, private, no broker intervention"""

    AutomatedExecutionOrderPublic: str = ...
    """Automated execution order, public, broker, intervention OK"""

    ManualOrder: str = ...
    """Staged order, broker intervention required"""


class TradingTechnologiesOrderProperties(QuantConnect.Orders.FixOrderProperites):
    """Trading Technologies order properties"""


class TimeInForceJsonConverter(JsonConverter):
    """Provides an implementation of JsonConverter that can deserialize TimeInForce objects"""

    @property
    def CanWrite(self) -> bool:
        """Gets a value indicating whether this Newtonsoft.Json.JsonConverter can write JSON."""
        ...

    def CanConvert(self, objectType: typing.Type) -> bool:
        """
        Determines whether this instance can convert the specified object type.
        
        :param objectType: Type of the object.
        :returns: true if this instance can convert the specified object type; otherwise, false.
        """
        ...

    def ReadJson(self, reader: typing.Any, objectType: typing.Type, existingValue: typing.Any, serializer: typing.Any) -> System.Object:
        """
        Reads the JSON representation of the object.
        
        :param reader: The Newtonsoft.Json.JsonReader to read from.
        :param objectType: Type of the object.
        :param existingValue: The existing value of object being read.
        :param serializer: The calling serializer.
        :returns: The object value.
        """
        ...

    def WriteJson(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """
        Writes the JSON representation of the object.
        
        :param writer: The Newtonsoft.Json.JsonWriter to write to.
        :param value: The value.
        :param serializer: The calling serializer.
        """
        ...


class OrderError(System.Enum):
    """Specifies the possible error states during presubmission checks"""

    CanNotUpdateFilledOrder = -8
    """Order has already been filled and cannot be modified (-8)"""

    GeneralError = -7
    """General error in order (-7)"""

    TimestampError = -6
    """Order timestamp error. Order appears to be executing in the future (-6)"""

    MaxOrdersExceeded = -5
    """Exceeded maximum allowed orders for one analysis period (-5)"""

    InsufficientCapital = -4
    """Insufficient capital to execute order (-4)"""

    MarketClosed = -3
    """Attempting market order outside of market hours (-3)"""

    NoData = -2
    """There is no data yet for this security - please wait for data (market order price not available yet) (-2)"""

    ZeroQuantity = -1
    """Order quantity must not be zero (-1)"""

    # Cannot convert to Python: None = 0
    """The order is OK (0)"""


class OrderUpdateEvent(System.Object):
    """
    Event that fires each time an order is updated in the brokerage side.
    These are not status changes but mainly price changes, like the stop price of a trailing stop order.
    """

    @property
    def OrderId(self) -> int:
        """The order ID."""
        ...

    @property
    def TrailingStopPrice(self) -> float:
        """The updated stop price for a TrailingStopOrder"""
        ...

    @property
    def StopTriggered(self) -> bool:
        """Flag indicating whether stop has been triggered for a StopLimitOrder"""
        ...


class OrderRequestType(System.Enum):
    """Specifies the type of OrderRequest"""

    Submit = 0
    """The request is a SubmitOrderRequest (0)"""

    Update = 1
    """The request is a UpdateOrderRequest (1)"""

    Cancel = 2
    """The request is a CancelOrderRequest (2)"""


class MarketOnOpenOrder(QuantConnect.Orders.Order):
    """Market on Open order type, submits a market order when the exchange opens"""

    @property
    def Type(self) -> int:
        """
        MarketOnOpen Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Intiializes a new instance of the MarketOnOpenOrder class."""
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, time: typing.Union[datetime.datetime, datetime.date], tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        Intiializes a new instance of the MarketOnOpenOrder class.
        
        :param symbol: The security's symbol being ordered
        :param quantity: The number of units to order
        :param time: The current time
        :param tag: A user defined tag for the order
        :param properties: The order properties for this order
        """
        ...

    def Clone(self) -> QuantConnect.Orders.Order:
        """
        Creates a deep-copy clone of this order
        
        :returns: A copy of this order.
        """
        ...

    def GetValueImpl(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the order value in units of the security's quote currency
        
        This method is protected.
        
        :param security: The security matching this order's symbol
        """
        ...


class GroupOrderExtensions(System.Object):
    """Group (combo) orders extension methods for easiest combo order manipulation"""

    @staticmethod
    def GetErrorMessage(securities: System.Collections.Generic.Dictionary[QuantConnect.Orders.Order, QuantConnect.Securities.Security], hasSufficientBuyingPowerResult: QuantConnect.Securities.HasSufficientBuyingPowerForOrderResult) -> str:
        ...

    @staticmethod
    def GetOrderLegGroupQuantity(legRatio: float, groupOrderManager: QuantConnect.Orders.GroupOrderManager) -> float:
        """
        Gets the combo order leg group quantity, that is, the total number of shares to be bought/sold from this leg,
        from its ratio and the group order quantity
        
        :param legRatio: The leg ratio
        :param groupOrderManager: The group order manager
        :returns: The total number of shares to be bought/sold from this leg.
        """
        ...

    @staticmethod
    def GetOrderLegRatio(legGroupQuantity: float, groupOrderManager: QuantConnect.Orders.GroupOrderManager) -> float:
        """
        Gets the combo order leg ratio from its group quantity and the group order quantity
        
        :param legGroupQuantity: The total number of shares to be bought/sold from this leg, that is, the result of the let ratio times the group quantity
        :param groupOrderManager: The group order manager
        :returns: The ratio of this combo order leg.
        """
        ...

    @staticmethod
    def TryGetGroupOrders(order: QuantConnect.Orders.Order, orderProvider: typing.Callable[[int], QuantConnect.Orders.Order], orders: typing.Optional[System.Collections.Generic.List[QuantConnect.Orders.Order]]) -> typing.Union[bool, System.Collections.Generic.List[QuantConnect.Orders.Order]]:
        """
        Gets the grouped orders (legs) of a group order
        
        :param order: Target order, which can be any of the legs of the combo
        :param orderProvider: Order provider to use to access the existing orders
        :param orders: List of orders in the combo
        :returns: False if any of the orders in the combo is not yet found in the order provider. True otherwise.
        """
        ...

    @staticmethod
    def TryGetGroupOrdersSecurities(orders: System.Collections.Generic.List[QuantConnect.Orders.Order], securityProvider: QuantConnect.Securities.ISecurityProvider, securities: typing.Optional[System.Collections.Generic.Dictionary[QuantConnect.Orders.Order, QuantConnect.Securities.Security]]) -> typing.Union[bool, System.Collections.Generic.Dictionary[QuantConnect.Orders.Order, QuantConnect.Securities.Security]]:
        """
        Gets the securities corresponding to each order in the group
        
        :param orders: List of orders to map
        :param securityProvider: The security provider to use
        :param securities: The resulting map of order to security
        :returns: True if the mapping is successful, false otherwise.
        """
        ...


class OrdersResponseWrapper(QuantConnect.Api.RestResponse):
    """Collection container for a list of orders for a project"""

    @property
    def Orders(self) -> System.Collections.Generic.List[QuantConnect.Orders.Order]:
        """Collection of summarized Orders objects"""
        ...


class GDAXOrderProperties(QuantConnect.Orders.OrderProperties):
    """Contains additional properties and settings for an order submitted to GDAX brokerage"""

    @property
    def PostOnly(self) -> bool:
        """
        This flag will ensure the order executes only as a maker (no fee) order.
        If part of the order results in taking liquidity rather than providing,
        it will be rejected and no part of the order will execute.
        Note: this flag is only applied to Limit orders.
        """
        ...

    def Clone(self) -> QuantConnect.Interfaces.IOrderProperties:
        """Returns a new instance clone of this object"""
        ...


class LimitOrder(QuantConnect.Orders.Order):
    """Limit order type definition"""

    @property
    def LimitPrice(self) -> float:
        """Limit price for this order."""
        ...

    @property
    def Type(self) -> int:
        """
        Limit Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Added a default constructor for JSON Deserialization:"""
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, limitPrice: float, time: typing.Union[datetime.datetime, datetime.date], tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New limit order constructor
        
        :param symbol: Symbol asset we're seeking to trade
        :param quantity: Quantity of the asset we're seeking to trade
        :param limitPrice: Price the order should be filled at if a limit order
        :param time: Time the order was placed
        :param tag: User defined data tag for this order
        :param properties: The order properties for this order
        """
        ...

    def ApplyUpdateOrderRequest(self, request: QuantConnect.Orders.UpdateOrderRequest) -> None:
        """
        Modifies the state of this order to match the update request
        
        :param request: The request to update this order object
        """
        ...

    def Clone(self) -> QuantConnect.Orders.Order:
        """
        Creates a deep-copy clone of this order
        
        :returns: A copy of this order.
        """
        ...

    def GetValueImpl(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the order value in units of the security's quote currency
        
        This method is protected.
        
        :param security: The security matching this order's symbol
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class ComboLegLimitOrder(QuantConnect.Orders.LimitOrder):
    """Combo leg limit order type"""

    @property
    def Type(self) -> int:
        """
        Combo Limit Leg Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Added a default constructor for JSON Deserialization:"""
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, limitPrice: float, time: typing.Union[datetime.datetime, datetime.date], groupOrderManager: QuantConnect.Orders.GroupOrderManager, tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New limit order constructor
        
        :param symbol: Symbol asset we're seeking to trade
        :param quantity: Quantity of the asset we're seeking to trade
        :param limitPrice: Price the order should be filled at if a limit order
        :param time: Time the order was placed
        :param groupOrderManager: Manager for the orders in the group
        :param tag: User defined data tag for this order
        :param properties: The order properties for this order
        """
        ...

    def Clone(self) -> QuantConnect.Orders.Order:
        """
        Creates a deep-copy clone of this order
        
        :returns: A copy of this order.
        """
        ...


class IndiaOrderProperties(QuantConnect.Orders.OrderProperties):
    """Contains additional properties and settings for an order submitted to Indian Brokerages"""

    class IndiaProductType(System.Enum):
        """Define the India Order type that we are targeting (MIS/CNC/NRML)."""

        MIS = 0
        """Margin Intraday Square Off (0)"""

        CNC = 1
        """Cash and Carry (1)"""

        NRML = 2
        """Normal (2)"""

    @property
    def ProductType(self) -> str:
        """India product type"""
        ...

    @overload
    def __init__(self, exchange: QuantConnect.Exchange) -> None:
        """
        Initialize a new OrderProperties for IndiaOrderProperties
        
        :param exchange: Exchange value, nse/bse etc
        """
        ...

    @overload
    def __init__(self, exchange: QuantConnect.Exchange, productType: QuantConnect.Orders.IndiaOrderProperties.IndiaProductType) -> None:
        """
        Initialize a new OrderProperties for IndiaOrderProperties
        
        :param exchange: Exchange value, nse/bse etc
        :param productType: ProductType value, MIS/CNC/NRML etc
        """
        ...

    def Clone(self) -> QuantConnect.Interfaces.IOrderProperties:
        """Returns a new instance clone of this object"""
        ...


class ComboLimitOrder(QuantConnect.Orders.Order):
    """Combo limit order type"""

    @property
    def Type(self) -> int:
        """
        Combo Limit Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @overload
    def __init__(self) -> None:
        """Added a default constructor for JSON Deserialization:"""
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, limitPrice: float, time: typing.Union[datetime.datetime, datetime.date], groupOrderManager: QuantConnect.Orders.GroupOrderManager, tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New limit order constructor
        
        :param symbol: Symbol asset we're seeking to trade
        :param quantity: Quantity of the asset we're seeking to trade
        :param limitPrice: Price the order should be filled at if a limit order
        :param time: Time the order was placed
        :param groupOrderManager: Manager for the orders in the group
        :param tag: User defined data tag for this order
        :param properties: The order properties for this order
        """
        ...

    def ApplyUpdateOrderRequest(self, request: QuantConnect.Orders.UpdateOrderRequest) -> None:
        """
        Modifies the state of this order to match the update request
        
        :param request: The request to update this order object
        """
        ...

    def Clone(self) -> QuantConnect.Orders.Order:
        """
        Creates a deep-copy clone of this order
        
        :returns: A copy of this order.
        """
        ...

    def GetValueImpl(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the order value in units of the security's quote currency
        
        This method is protected.
        
        :param security: The security matching this order's symbol
        """
        ...


class WolverineOrderProperties(QuantConnect.Orders.OrderProperties):
    """Wolverine order properties"""

    @property
    def ExchangePostFix(self) -> str:
        """The exchange post fix to apply if any"""
        ...


class BitfinexOrderProperties(QuantConnect.Orders.OrderProperties):
    """Contains additional properties and settings for an order submitted to Bitfinex brokerage"""

    @property
    def PostOnly(self) -> bool:
        """
        This flag will ensure the order executes only as a maker (no fee) order.
        If part of the order results in taking liquidity rather than providing,
        it will be rejected and no part of the order will execute.
        Note: this flag is only applied to Limit orders.
        """
        ...

    @property
    def Hidden(self) -> bool:
        """
        The hidden order option ensures an order does not appear in the order book; thus does not influence other market participants.
        If you place a hidden order, you will always pay the taker fee. If you place a limit order that hits a hidden order, you will always pay the maker fee.
        """
        ...

    def Clone(self) -> QuantConnect.Interfaces.IOrderProperties:
        """Returns a new instance clone of this object"""
        ...


class BinanceOrderProperties(QuantConnect.Orders.OrderProperties):
    """Contains additional properties and settings for an order submitted to Binance brokerage"""

    @property
    def PostOnly(self) -> bool:
        """
        This flag will ensure the order executes only as a maker (no fee) order.
        If part of the order results in taking liquidity rather than providing,
        it will be rejected and no part of the order will execute.
        Note: this flag is only applied to Limit orders.
        """
        ...

    def Clone(self) -> QuantConnect.Interfaces.IOrderProperties:
        """Returns a new instance clone of this object"""
        ...


class LimitIfTouchedOrder(QuantConnect.Orders.Order):
    """
    In effect, a LimitIfTouchedOrder behaves opposite to the StopLimitOrder;
    after a trigger price is touched, a limit order is set for some user-defined value above (below)
    the trigger when selling (buying).
    https://www.interactivebrokers.ca/en/index.php?f=45318
    """

    @property
    def Type(self) -> int:
        """
        Order Type
        
        This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
        """
        ...

    @property
    def TriggerPrice(self) -> float:
        """The price which, when touched, will trigger the setting of a limit order at LimitPrice."""
        ...

    @property
    def LimitPrice(self) -> float:
        """The price at which to set the limit order following TriggerPrice being touched."""
        ...

    @property
    def TriggerTouched(self) -> bool:
        """Whether or not the TriggerPrice has been touched."""
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float, triggerPrice: typing.Optional[float], limitPrice: float, time: typing.Union[datetime.datetime, datetime.date], tag: str = ..., properties: QuantConnect.Interfaces.IOrderProperties = None) -> None:
        """
        New LimitIfTouchedOrder constructor.
        
        :param symbol: Symbol asset we're seeking to trade
        :param quantity: Quantity of the asset we're seeking to trade
        :param triggerPrice: Price which must be touched in order to then set a limit order
        :param limitPrice: Maximum price to fill the order
        :param time: Time the order was placed
        :param tag: User defined data tag for this order
        :param properties: The order properties for this order
        """
        ...

    @overload
    def __init__(self) -> None:
        """Default constructor for JSON Deserialization:"""
        ...

    def ApplyUpdateOrderRequest(self, request: QuantConnect.Orders.UpdateOrderRequest) -> None:
        """
        Modifies the state of this order to match the update request
        
        :param request: The request to update this order object
        """
        ...

    def Clone(self) -> QuantConnect.Orders.Order:
        """
        Creates a deep-copy clone of this order
        
        :returns: A copy of this order.
        """
        ...

    def GetValueImpl(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the order value in units of the security's quote currency for a single unit.
        A single unit here is a single share of stock, or a single barrel of oil, or the
        cost of a single share in an option contract.
        
        This method is protected.
        
        :param security: The security matching this order's symbol
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class OrderExtensions(System.Object):
    """Provides extension methods for the Order class and for the OrderStatus enumeration"""

    @staticmethod
    def IsClosed(status: QuantConnect.Orders.OrderStatus) -> bool:
        """
        Determines if the specified status is in a closed state.
        
        :param status: The status to check
        :returns: True if the status is OrderStatus.Filled, OrderStatus.Canceled, or OrderStatus.Invalid.
        """
        ...

    @staticmethod
    def IsFill(status: QuantConnect.Orders.OrderStatus) -> bool:
        """
        Determines if the specified status is a fill, that is, OrderStatus.Filled
        order OrderStatus.PartiallyFilled
        
        :param status: The status to check
        :returns: True if the status is OrderStatus.Filled or OrderStatus.PartiallyFilled, false otherwise.
        """
        ...

    @staticmethod
    def IsLimitOrder(orderType: QuantConnect.Orders.OrderType) -> bool:
        """
        Determines whether or not the specified order is a limit order
        
        :param orderType: The order to check
        :returns: True if the order is a limit order, false otherwise.
        """
        ...

    @staticmethod
    def IsOpen(status: QuantConnect.Orders.OrderStatus) -> bool:
        """
        Determines if the specified status is in an open state.
        
        :param status: The status to check
        :returns: True if the status is not OrderStatus.Filled, OrderStatus.Canceled, or OrderStatus.Invalid.
        """
        ...

    @staticmethod
    def IsStopOrder(orderType: QuantConnect.Orders.OrderType) -> bool:
        """
        Determines whether or not the specified order is a stop order
        
        :param orderType: The order to check
        :returns: True if the order is a stop order, false otherwise.
        """
        ...


class Leg(System.Object):
    """Basic order leg"""

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        """The legs symbol"""
        ...

    @property
    def Quantity(self) -> int:
        """Quantity multiplier used to specify proper scale (and direction) of the leg within the strategy"""
        ...

    @property
    def OrderPrice(self) -> typing.Optional[float]:
        """Order limit price of the leg in case limit order is sent to the market on strategy execution"""
        ...

    @staticmethod
    def Create(symbol: typing.Union[QuantConnect.Symbol, str], quantity: int, limitPrice: typing.Optional[float] = None) -> QuantConnect.Orders.Leg:
        """
        Creates a new instance
        
        :param symbol: The symbol
        :param quantity: The quantity
        :param limitPrice: Associated limit price if any
        """
        ...


class BrokerageOrderIdChangedEvent(System.Object):
    """Event used when the brokerage order id has changed"""

    @property
    def OrderId(self) -> int:
        """The order ID."""
        ...

    @property
    def BrokerId(self) -> System.Collections.Generic.List[str]:
        """Brokerage Id for this order"""
        ...


class FTXOrderProperties(QuantConnect.Orders.OrderProperties):
    """Contains additional properties and settings for an order submitted to FTX brokerage"""

    @property
    def PostOnly(self) -> bool:
        """
        This flag will ensure the order executes only as a maker (maker fee) order.
        If part of the order results in taking liquidity rather than providing,
        it will be rejected and no part of the order will execute.
        Note: this flag is only applied to Limit orders.
        """
        ...

    @property
    def ReduceOnly(self) -> bool:
        """If you send a reduce only order, it will only trade if it would decrease your position size."""
        ...

    def Clone(self) -> QuantConnect.Interfaces.IOrderProperties:
        """Returns a new instance clone of this object"""
        ...


