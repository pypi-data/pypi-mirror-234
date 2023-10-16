from typing import overload
import datetime
import typing

import QuantConnect
import QuantConnect.Algorithm.Framework.Alphas
import QuantConnect.Algorithm.Framework.Alphas.Analysis
import QuantConnect.Interfaces
import System.Collections.Generic


class InsightManager(QuantConnect.Algorithm.Framework.Alphas.InsightCollection):
    """Encapsulates the storage of insights."""

    def __init__(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        """
        Creates a new instance
        
        :param algorithm: The associated algorithm instance
        """
        ...

    @overload
    def Cancel(self, symbols: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]) -> None:
        """
        Cancel the insights of the given symbols
        
        :param symbols: Symbol we want to cancel insights for
        """
        ...

    @overload
    def Cancel(self, insights: System.Collections.Generic.IEnumerable[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> None:
        """
        Cancel the given insights
        
        :param insights: Insights to cancel
        """
        ...

    @overload
    def Expire(self, symbols: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]) -> None:
        """
        Expire the insights of the given symbols
        
        :param symbols: Symbol we want to expire insights for
        """
        ...

    @overload
    def Expire(self, insights: System.Collections.Generic.IEnumerable[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> None:
        """
        Expire the given insights
        
        :param insights: Insights to expire
        """
        ...

    @overload
    def SetInsightScoreFunction(self, insightScoreFunction: QuantConnect.Algorithm.Framework.Alphas.IInsightScoreFunction) -> None:
        """
        Sets the insight score function to use
        
        :param insightScoreFunction: Model that scores insights
        """
        ...

    @overload
    def SetInsightScoreFunction(self, insightScoreFunction: typing.Any) -> None:
        """
        Sets the insight score function to use
        
        :param insightScoreFunction: Model that scores insights
        """
        ...

    def Step(self, utcNow: typing.Union[datetime.datetime, datetime.date]) -> None:
        """
        Process a new time step handling insights scoring
        
        :param utcNow: The current utc time
        """
        ...


