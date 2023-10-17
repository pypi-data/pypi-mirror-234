from typing import overload
import QuantConnect.Securities.FutureOption.Api
import System
import System.Collections.Generic


class CMEOptionChainQuoteEntry(System.Object):
    """Option chain entry quotes, containing strike price"""

    @property
    def StrikePrice(self) -> float:
        """Strike price of the future option quote entry"""
        ...


class CMEOptionChainQuotes(System.Object):
    """CME Option Chain Quotes API call root response"""

    @property
    def Quotes(self) -> System.Collections.Generic.List[QuantConnect.Securities.FutureOption.Api.CMEOptionChainQuoteEntry]:
        """The future options contracts with/without settlements"""
        ...


class CMEProductSlateV2ListEntry(System.Object):
    """Product entry describing the asset matching the search criteria"""

    @property
    def Id(self) -> int:
        """CME ID for the asset"""
        ...

    @property
    def Name(self) -> str:
        """Name of the product (e.g. E-mini NASDAQ futures)"""
        ...

    @property
    def Clearing(self) -> str:
        """Clearing code"""
        ...

    @property
    def Globex(self) -> str:
        """GLOBEX ticker"""
        ...

    @property
    def GlobexTraded(self) -> bool:
        """Is traded in the GLOBEX venue"""
        ...

    @property
    def Venues(self) -> str:
        """Venues this asset trades on"""
        ...

    @property
    def Cleared(self) -> str:
        """Asset type this product is cleared as (i.e. "Futures", "Options")"""
        ...

    @property
    def Exchange(self) -> str:
        """Exchange the asset trades on (i.e. CME, NYMEX, COMEX, CBOT)"""
        ...

    @property
    def GroupId(self) -> int:
        """Asset class group ID - describes group of asset class (e.g. equities, agriculture, etc.)"""
        ...

    @property
    def subGroupId(self) -> int:
        """More specific ID describing product"""
        ...


class CMEProductSlateV2ListResponse(System.Object):
    """Product slate API call root response"""

    @property
    def Products(self) -> System.Collections.Generic.List[QuantConnect.Securities.FutureOption.Api.CMEProductSlateV2ListEntry]:
        """Products matching the search criteria"""
        ...


class CMEOptionExpirationEntry(System.Object):
    """Chicago Mercantile Exchange Option Expiration Entry"""

    @property
    def Month(self) -> int:
        """Month of expiry"""
        ...

    @property
    def Year(self) -> int:
        """Year of expiry"""
        ...

    @property
    def Code(self) -> str:
        """Expiration code (two letter)"""
        ...

    @property
    def TwoDigitsCode(self) -> str:
        """Expiration code (three letter)"""
        ...


class CMEOptionsExpiration(System.Object):
    """
    Future options Expiration entries. These are useful because we can derive the
    future chain from this data, since FOP and FUT share a 1-1 expiry code.
    """

    @property
    def Label(self) -> str:
        """Date of expiry"""
        ...

    @property
    def ProductId(self) -> int:
        """Product ID of the expiring asset (usually future option)"""
        ...

    @property
    def ContractId(self) -> str:
        """Contract ID of the asset"""
        ...

    @property
    def Expiration(self) -> QuantConnect.Securities.FutureOption.Api.CMEOptionExpirationEntry:
        """Contract month code formatted as [FUTURE_MONTH_LETTER(1)][YEAR(1)]"""
        ...


class CMEOptionsTradeDatesAndExpiration(System.Object):
    """CME options trades, dates, and expiration list API call root response"""

    @property
    def Label(self) -> str:
        """Describes the type of future option this entry is"""
        ...

    @property
    def Name(self) -> str:
        """Name of the product"""
        ...

    @property
    def OptionType(self) -> str:
        """
        Option type. "AME" for American, "EUR" for European.
        Note that there are other types such as weekly, but we
        only support American options for now.
        """
        ...

    @property
    def ProductId(self) -> int:
        """Product ID of the option"""
        ...

    @property
    def Daily(self) -> bool:
        """Is Daily option"""
        ...

    @property
    def Sto(self) -> bool:
        """???"""
        ...

    @property
    def Weekly(self) -> bool:
        """Is weekly option"""
        ...

    @property
    def Expirations(self) -> System.Collections.Generic.List[QuantConnect.Securities.FutureOption.Api.CMEOptionsExpiration]:
        """Expirations of the future option"""
        ...


