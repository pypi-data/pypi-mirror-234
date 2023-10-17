from typing import overload
import abc

import QuantConnect
import QuantConnect.Packets
import QuantConnect.Report.ReportElements
import System


class ReportElement(System.Object, QuantConnect.Report.ReportElements.IReportElement, metaclass=abc.ABCMeta):
    """Common interface for template elements of the report"""

    @property
    def Name(self) -> str:
        """Name of this report element"""
        ...

    @property
    def Key(self) -> str:
        """Template key code."""
        ...

    @property
    def JsonKey(self) -> str:
        """Normalizes the key into a JSON-friendly key"""
        ...

    @property
    def Result(self) -> System.Object:
        """Result of the render as an object for serialization to JSON"""
        ...

    def Render(self) -> str:
        """The generated output string to be injected"""
        ...


class ParametersReportElement(QuantConnect.Report.ReportElements.ReportElement):
    """This class has no documentation."""

    def __init__(self, name: str, key: str, backtestConfiguration: QuantConnect.AlgorithmConfiguration, liveConfiguration: QuantConnect.AlgorithmConfiguration, template: str) -> None:
        """
        Creates a two column table for the Algorithm's Parameters
        
        :param name: Name of the widget
        :param key: Location of injection
        :param backtestConfiguration: The configuration of the backtest algorithm
        :param liveConfiguration: The configuration of the live algorithm
        :param template: HTML template to use
        """
        ...

    def Render(self) -> str:
        """
        Generates a HTML two column table for the Algorithm's Parameters
        
        :returns: Returns a string representing a HTML two column table.
        """
        ...


class EstimatedCapacityReportElement(QuantConnect.Report.ReportElements.ReportElement):
    """Capacity Estimation Report Element"""

    def __init__(self, name: str, key: str, backtest: QuantConnect.Packets.BacktestResult, live: QuantConnect.Packets.LiveResult) -> None:
        """
        Create a new capacity estimate
        
        :param name: Name of the widget
        :param key: Location of injection
        :param backtest: Backtest result object
        :param live: Live result object
        """
        ...

    def Render(self) -> str:
        """Render element"""
        ...


