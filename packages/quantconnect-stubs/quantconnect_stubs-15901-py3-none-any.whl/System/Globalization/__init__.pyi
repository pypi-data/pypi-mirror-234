from typing import overload
import abc
import datetime
import typing
import warnings

import System
import System.Collections
import System.Globalization
import System.Reflection
import System.Runtime.Serialization
import System.Text

System_Globalization_SortVersion = typing.Any


class CalendarWeekRule(System.Enum):
    """This class has no documentation."""

    FirstDay = 0

    FirstFullWeek = 1

    FirstFourDayWeek = 2


class Calendar(System.Object, System.ICloneable, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def AlgorithmType(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CalendarAlgorithmType enum."""
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    CurrentEra: int = 0

    @property
    @abc.abstractmethod
    def Eras(self) -> typing.List[int]:
        """Get the list of era values."""
        ...

    @property
    def DaysInYearBeforeMinSupportedYear(self) -> int:
        """This property is protected."""
        ...

    @property
    def TwoDigitYearMax(self) -> int:
        """
        Returns and assigns the maximum value to represent a two digit year.
        This value is the upper boundary of a 100 year range that allows a
        two digit year to be properly translated to a four digit year.
        For example, if 2049 is the upper boundary, then a two digit value of
        30 should be interpreted as 1950 while a two digit value of 49 should
        be interpreted as 2049.  In this example, the 100 year range would be
        from 1950-2049.  See ToFourDigitYear().
        """
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def AddDays(self, time: typing.Union[datetime.datetime, datetime.date], days: int) -> datetime.datetime:
        """
        Returns the DateTime resulting from adding a fractional number of
        days to the specified DateTime. The result is computed by rounding the
        fractional number of days given by value to the nearest
        millisecond, and adding that interval to the specified DateTime. The
        value argument is permitted to be negative.
        """
        ...

    def AddHours(self, time: typing.Union[datetime.datetime, datetime.date], hours: int) -> datetime.datetime:
        """
        Returns the DateTime resulting from adding a fractional number of
        hours to the specified DateTime. The result is computed by rounding the
        fractional number of hours given by value to the nearest
        millisecond, and adding that interval to the specified DateTime. The
        value argument is permitted to be negative.
        """
        ...

    def AddMilliseconds(self, time: typing.Union[datetime.datetime, datetime.date], milliseconds: float) -> datetime.datetime:
        """
        Returns the DateTime resulting from adding the given number of
        milliseconds to the specified DateTime. The result is computed by rounding
        the number of milliseconds given by value to the nearest integer,
        and adding that interval to the specified DateTime. The value
        argument is permitted to be negative.
        """
        ...

    def AddMinutes(self, time: typing.Union[datetime.datetime, datetime.date], minutes: int) -> datetime.datetime:
        """
        Returns the DateTime resulting from adding a fractional number of
        minutes to the specified DateTime. The result is computed by rounding the
        fractional number of minutes given by value to the nearest
        millisecond, and adding that interval to the specified DateTime. The
        value argument is permitted to be negative.
        """
        ...

    def AddMonths(self, time: typing.Union[datetime.datetime, datetime.date], months: int) -> datetime.datetime:
        """
        Returns the DateTime resulting from adding the given number of
        months to the specified DateTime. The result is computed by incrementing
        (or decrementing) the year and month parts of the specified DateTime by
        value months, and, if required, adjusting the day part of the
        resulting date downwards to the last day of the resulting month in the
        resulting year. The time-of-day part of the result is the same as the
        time-of-day part of the specified DateTime.
        
        In more precise terms, considering the specified DateTime to be of the
        form y / m / d + t, where y is the
        year, m is the month, d is the day, and t is the
        time-of-day, the result is y1 / m1 / d1 + t,
        where y1 and m1 are computed by adding value months
        to y and m, and d1 is the largest value less than
        or equal to d that denotes a valid day in month m1 of year
        y1.
        """
        ...

    def AddSeconds(self, time: typing.Union[datetime.datetime, datetime.date], seconds: int) -> datetime.datetime:
        """
        Returns the DateTime resulting from adding a number of
        seconds to the specified DateTime. The result is computed by rounding the
        fractional number of seconds given by value to the nearest
        millisecond, and adding that interval to the specified DateTime. The
        value argument is permitted to be negative.
        """
        ...

    def AddWeeks(self, time: typing.Union[datetime.datetime, datetime.date], weeks: int) -> datetime.datetime:
        ...

    def AddYears(self, time: typing.Union[datetime.datetime, datetime.date], years: int) -> datetime.datetime:
        """
        Returns the DateTime resulting from adding the given number of
        years to the specified DateTime. The result is computed by incrementing
        (or decrementing) the year part of the specified DateTime by value
        years. If the month and day of the specified DateTime is 2/29, and if the
        resulting year is not a leap year, the month and day of the resulting
        DateTime becomes 2/28. Otherwise, the month, day, and time-of-day
        parts of the result are the same as those of the specified DateTime.
        """
        ...

    def Clone(self) -> System.Object:
        ...

    def GetDayOfMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the day-of-month part of the specified DateTime. The returned
        value is an integer between 1 and 31.
        """
        ...

    def GetDayOfWeek(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the day-of-week part of the specified DateTime. The returned value
        is an integer between 0 and 6, where 0 indicates Sunday, 1 indicates
        Monday, 2 indicates Tuesday, 3 indicates Wednesday, 4 indicates
        Thursday, 5 indicates Friday, and 6 indicates Saturday.
        
        :returns: This method returns the int value of a member of the System.DayOfWeek enum.
        """
        ...

    def GetDayOfYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the day-of-year part of the specified DateTime. The returned value
        is an integer between 1 and 366.
        """
        ...

    @overload
    def GetDaysInMonth(self, year: int, month: int) -> int:
        """
        Returns the number of days in the month given by the year and
        month arguments.
        """
        ...

    @overload
    def GetDaysInMonth(self, year: int, month: int, era: int) -> int:
        """
        Returns the number of days in the month given by the year and
        month arguments for the specified era.
        """
        ...

    @overload
    def GetDaysInYear(self, year: int) -> int:
        """
        Returns the number of days in the year given by the year argument
        for the current era.
        """
        ...

    @overload
    def GetDaysInYear(self, year: int, era: int) -> int:
        """
        Returns the number of days in the year given by the year argument
        for the current era.
        """
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """Returns the era for the specified DateTime value."""
        ...

    def GetHour(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    @overload
    def GetLeapMonth(self, year: int) -> int:
        """
        Returns  the leap month in a calendar year of the current era.
        This method returns 0 if this calendar does not have leap month,
        or this year is not a leap year.
        """
        ...

    @overload
    def GetLeapMonth(self, year: int, era: int) -> int:
        """
        Returns  the leap month in a calendar year of the specified era.
        This method returns 0 if this calendar does not have leap month,
        or this year is not a leap year.
        """
        ...

    def GetMilliseconds(self, time: typing.Union[datetime.datetime, datetime.date]) -> float:
        ...

    def GetMinute(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    @overload
    def GetMonthsInYear(self, year: int) -> int:
        ...

    @overload
    def GetMonthsInYear(self, year: int, era: int) -> int:
        ...

    def GetSecond(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetWeekOfYear(self, time: typing.Union[datetime.datetime, datetime.date], rule: System.Globalization.CalendarWeekRule, firstDayOfWeek: System.DayOfWeek) -> int:
        """
        Returns the week of year for the specified DateTime. The returned value is an
        integer between 1 and 53.
        """
        ...

    def GetYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the year part of the specified DateTime. The returned value is an
        integer between 1 and 9999.
        """
        ...

    @overload
    def IsLeapDay(self, year: int, month: int, day: int) -> bool:
        """
        Checks whether a given day in the current era is a leap day.
        This method returns true if the date is a leap day, or false if not.
        """
        ...

    @overload
    def IsLeapDay(self, year: int, month: int, day: int, era: int) -> bool:
        """
        Checks whether a given day in the specified era is a leap day.
        This method returns true if the date is a leap day, or false if not.
        """
        ...

    @overload
    def IsLeapMonth(self, year: int, month: int) -> bool:
        """
        Checks whether a given month in the current era is a leap month.
        This method returns true if month is a leap month, or false if not.
        """
        ...

    @overload
    def IsLeapMonth(self, year: int, month: int, era: int) -> bool:
        """
        Checks whether a given month in the specified era is a leap month. This method returns true if
        month is a leap month, or false if not.
        """
        ...

    @overload
    def IsLeapYear(self, year: int) -> bool:
        """
        Checks whether a given year in the current era is a leap year.
        This method returns true if year is a leap year, or false if not.
        """
        ...

    @overload
    def IsLeapYear(self, year: int, era: int) -> bool:
        """
        Checks whether a given year in the specified era is a leap year.
        This method returns true if year is a leap year, or false if not.
        """
        ...

    @staticmethod
    def ReadOnly(calendar: System.Globalization.Calendar) -> System.Globalization.Calendar:
        ...

    @overload
    def ToDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int) -> datetime.datetime:
        """
        Returns the date and time converted to a DateTime value.
        Throws an exception if the n-tuple is invalid.
        """
        ...

    @overload
    def ToDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, era: int) -> datetime.datetime:
        """
        Returns the date and time converted to a DateTime value.
        Throws an exception if the n-tuple is invalid.
        """
        ...

    def ToFourDigitYear(self, year: int) -> int:
        """
        Converts the year value to the appropriate century by using the
        TwoDigitYearMax property.  For example, if the TwoDigitYearMax value is 2049,
        then a two digit value of 50 will get converted to 1950 while a two digit
        value of 49 will get converted to 2049.
        """
        ...


class ThaiBuddhistCalendar(System.Globalization.Calendar):
    """
    ThaiBuddhistCalendar is based on Gregorian calendar.
    Its year value has an offset to the Gregorain calendar.
    """

    ThaiBuddhistEra: int = 1

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def AlgorithmType(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CalendarAlgorithmType enum."""
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    @property
    def TwoDigitYearMax(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    def AddMonths(self, time: typing.Union[datetime.datetime, datetime.date], months: int) -> datetime.datetime:
        ...

    def AddYears(self, time: typing.Union[datetime.datetime, datetime.date], years: int) -> datetime.datetime:
        ...

    def GetDayOfMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDayOfWeek(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """:returns: This method returns the int value of a member of the System.DayOfWeek enum."""
        ...

    def GetDayOfYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDaysInMonth(self, year: int, month: int, era: int) -> int:
        ...

    def GetDaysInYear(self, year: int, era: int) -> int:
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetLeapMonth(self, year: int, era: int) -> int:
        ...

    def GetMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetMonthsInYear(self, year: int, era: int) -> int:
        ...

    def GetWeekOfYear(self, time: typing.Union[datetime.datetime, datetime.date], rule: System.Globalization.CalendarWeekRule, firstDayOfWeek: System.DayOfWeek) -> int:
        ...

    def GetYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def IsLeapDay(self, year: int, month: int, day: int, era: int) -> bool:
        ...

    def IsLeapMonth(self, year: int, month: int, era: int) -> bool:
        ...

    def IsLeapYear(self, year: int, era: int) -> bool:
        ...

    def ToDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, era: int) -> datetime.datetime:
        ...

    def ToFourDigitYear(self, year: int) -> int:
        ...


class SortVersion(System.Object, System.IEquatable[System_Globalization_SortVersion]):
    """This class has no documentation."""

    @property
    def FullVersion(self) -> int:
        ...

    @property
    def SortId(self) -> System.Guid:
        ...

    def __init__(self, fullVersion: int, sortId: System.Guid) -> None:
        ...

    @overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def Equals(self, other: System.Globalization.SortVersion) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class CompareOptions(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = ...

    IgnoreCase = ...

    IgnoreNonSpace = ...

    IgnoreSymbols = ...

    IgnoreKanaType = ...

    IgnoreWidth = ...

    OrdinalIgnoreCase = ...

    StringSort = ...

    Ordinal = ...


class SortKey(System.Object):
    """Represents the result of mapping a string to its sort key."""

    @property
    def OriginalString(self) -> str:
        """
        Returns the original string used to create the current instance
        of SortKey.
        """
        ...

    @property
    def KeyData(self) -> typing.List[int]:
        """
        Returns a byte array representing the current instance of the
        sort key.
        """
        ...

    @staticmethod
    def Compare(sortkey1: System.Globalization.SortKey, sortkey2: System.Globalization.SortKey) -> int:
        """
        Compares the two sort keys.  Returns 0 if the two sort keys are
        equal, a number less than 0 if sortkey1 is less than sortkey2,
        and a number greater than 0 if sortkey1 is greater than sortkey2.
        """
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    def ToString(self) -> str:
        ...


class CompareInfo(System.Object, System.Runtime.Serialization.IDeserializationCallback):
    """This class implements a set of methods for comparing strings."""

    @property
    def Name(self) -> str:
        """
        Returns the name of the culture (well actually, of the sort).
         Very important for providing a non-LCID way of identifying
         what the sort is.
        
         Note that this name isn't dereferenced in case the CompareInfo is a different locale
         which is consistent with the behaviors of earlier versions.  (so if you ask for a sort
         and the locale's changed behavior, then you'll get changed behavior, which is like
         what happens for a version update)
        """
        ...

    @property
    def Version(self) -> System.Globalization.SortVersion:
        ...

    @property
    def LCID(self) -> int:
        ...

    @overload
    def Compare(self, string1: str, string2: str) -> int:
        """
        Compares the two strings with the given options.  Returns 0 if the
        two strings are equal, a number less than 0 if string1 is less
        than string2, and a number greater than 0 if string1 is greater
        than string2.
        """
        ...

    @overload
    def Compare(self, string1: str, string2: str, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def Compare(self, string1: str, offset1: int, length1: int, string2: str, offset2: int, length2: int) -> int:
        """
        Compares the specified regions of the two strings with the given
        options.
        Returns 0 if the two strings are equal, a number less than 0 if
        string1 is less than string2, and a number greater than 0 if
        string1 is greater than string2.
        """
        ...

    @overload
    def Compare(self, string1: str, offset1: int, string2: str, offset2: int, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def Compare(self, string1: str, offset1: int, string2: str, offset2: int) -> int:
        ...

    @overload
    def Compare(self, string1: str, offset1: int, length1: int, string2: str, offset2: int, length2: int, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def Compare(self, string1: System.ReadOnlySpan[str], string2: System.ReadOnlySpan[str], options: System.Globalization.CompareOptions = ...) -> int:
        """
        Compares two strings.
        
        :param string1: The first string to compare.
        :param string2: The second string to compare.
        :param options: The CompareOptions to use during the comparison.
        :returns: Zero if  and  are equal; or a negative value if  sorts before ; or a positive value if  sorts after .
        """
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    @staticmethod
    @overload
    def GetCompareInfo(culture: int, assembly: System.Reflection.Assembly) -> System.Globalization.CompareInfo:
        """
        Get the CompareInfo constructed from the data table in the specified
        assembly for the specified culture.
        Warning: The assembly versioning mechanism is dead!
        """
        ...

    @staticmethod
    @overload
    def GetCompareInfo(name: str, assembly: System.Reflection.Assembly) -> System.Globalization.CompareInfo:
        """
        Get the CompareInfo constructed from the data table in the specified
        assembly for the specified culture.
        The purpose of this method is to provide version for CompareInfo tables.
        """
        ...

    @staticmethod
    @overload
    def GetCompareInfo(culture: int) -> System.Globalization.CompareInfo:
        """
        Get the CompareInfo for the specified culture.
        This method is provided for ease of integration with NLS-based software.
        """
        ...

    @staticmethod
    @overload
    def GetCompareInfo(name: str) -> System.Globalization.CompareInfo:
        """Get the CompareInfo for the specified culture."""
        ...

    @overload
    def GetHashCode(self) -> int:
        ...

    @overload
    def GetHashCode(self, source: str, options: System.Globalization.CompareOptions) -> int:
        """
        This method performs the equivalent of of creating a Sortkey for a string from CompareInfo,
        then generates a randomized hashcode value from the sort key.
        
        The hash code is guaranteed to be the same for string A and B where A.Equals(B) is true and both
        the CompareInfo and the CompareOptions are the same. If two different CompareInfo objects
        treat the string the same way, this implementation will treat them differently (the same way that
        Sortkey does at the moment).
        """
        ...

    @overload
    def GetHashCode(self, source: System.ReadOnlySpan[str], options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def GetSortKey(self, source: str, options: System.Globalization.CompareOptions) -> System.Globalization.SortKey:
        """Gets the SortKey for the given string with the given options."""
        ...

    @overload
    def GetSortKey(self, source: str) -> System.Globalization.SortKey:
        ...

    @overload
    def GetSortKey(self, source: System.ReadOnlySpan[str], destination: System.Span[int], options: System.Globalization.CompareOptions = ...) -> int:
        """
        Computes a sort key over the specified input.
        
        :param source: The text over which to compute the sort key.
        :param destination: The buffer into which to write the resulting sort key bytes.
        :param options: The CompareOptions used for computing the sort key.
        :returns: The number of bytes written to .
        """
        ...

    def GetSortKeyLength(self, source: System.ReadOnlySpan[str], options: System.Globalization.CompareOptions = ...) -> int:
        """
        Returns the length (in bytes) of the sort key that would be produced from the specified input.
        
        :param source: The text over which to compute the sort key.
        :param options: The CompareOptions used for computing the sort key.
        :returns: The length (in bytes) of the sort key.
        """
        ...

    @overload
    def IndexOf(self, source: str, value: str) -> int:
        """
        Returns the first index where value is found in string.  The
        search starts from startIndex and ends at endIndex.  Returns -1 if
        the specified value is not found.  If value equals string.Empty,
        startIndex is returned.  Throws IndexOutOfRange if startIndex or
        endIndex is less than zero or greater than the length of string.
        Throws ArgumentException if value (as a string) is null.
        """
        ...

    @overload
    def IndexOf(self, source: str, value: str) -> int:
        ...

    @overload
    def IndexOf(self, source: str, value: str, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def IndexOf(self, source: str, value: str, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def IndexOf(self, source: str, value: str, startIndex: int) -> int:
        ...

    @overload
    def IndexOf(self, source: str, value: str, startIndex: int) -> int:
        ...

    @overload
    def IndexOf(self, source: str, value: str, startIndex: int, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def IndexOf(self, source: str, value: str, startIndex: int, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def IndexOf(self, source: str, value: str, startIndex: int, count: int) -> int:
        ...

    @overload
    def IndexOf(self, source: str, value: str, startIndex: int, count: int) -> int:
        ...

    @overload
    def IndexOf(self, source: str, value: str, startIndex: int, count: int, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def IndexOf(self, source: str, value: str, startIndex: int, count: int, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def IndexOf(self, source: System.ReadOnlySpan[str], value: System.ReadOnlySpan[str], options: System.Globalization.CompareOptions = ...) -> int:
        """
        Searches for the first occurrence of a substring within a source string.
        
        :param source: The string to search within.
        :param value: The substring to locate within .
        :param options: The CompareOptions to use during the search.
        :returns: The zero-based index into  where the substring  first appears; or -1 if  cannot be found within .
        """
        ...

    @overload
    def IndexOf(self, source: System.ReadOnlySpan[str], value: System.ReadOnlySpan[str], options: System.Globalization.CompareOptions, matchLength: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Searches for the first occurrence of a substring within a source string.
        
        :param source: The string to search within.
        :param value: The substring to locate within .
        :param options: The CompareOptions to use during the search.
        :param matchLength: When this method returns, contains the number of characters of  that matched the desired value. This may be different than the length of  if a linguistic comparison is performed. Set to 0 if  is not found within .
        :returns: The zero-based index into  where the substring  first appears; or -1 if  cannot be found within .
        """
        ...

    @overload
    def IndexOf(self, source: System.ReadOnlySpan[str], value: System.Text.Rune, options: System.Globalization.CompareOptions = ...) -> int:
        """
        Searches for the first occurrence of a Rune within a source string.
        
        :param source: The string to search within.
        :param value: The Rune to locate within .
        :param options: The CompareOptions to use during the search.
        :returns: The zero-based index into  where  first appears; or -1 if  cannot be found within .
        """
        ...

    @overload
    def IsPrefix(self, source: str, prefix: str, options: System.Globalization.CompareOptions) -> bool:
        """
        Determines whether prefix is a prefix of string.  If prefix equals
        string.Empty, true is returned.
        """
        ...

    @overload
    def IsPrefix(self, source: System.ReadOnlySpan[str], prefix: System.ReadOnlySpan[str], options: System.Globalization.CompareOptions = ...) -> bool:
        """
        Determines whether a string starts with a specific prefix.
        
        :param source: The string to search within.
        :param prefix: The prefix to attempt to match at the start of .
        :param options: The CompareOptions to use during the match.
        :returns: true if  occurs at the start of ; otherwise, false.
        """
        ...

    @overload
    def IsPrefix(self, source: System.ReadOnlySpan[str], prefix: System.ReadOnlySpan[str], options: System.Globalization.CompareOptions, matchLength: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Determines whether a string starts with a specific prefix.
        
        :param source: The string to search within.
        :param prefix: The prefix to attempt to match at the start of .
        :param options: The CompareOptions to use during the match.
        :param matchLength: When this method returns, contains the number of characters of  that matched the desired prefix. This may be different than the length of  if a linguistic comparison is performed. Set to 0 if the prefix did not match.
        :returns: true if  occurs at the start of ; otherwise, false.
        """
        ...

    @overload
    def IsPrefix(self, source: str, prefix: str) -> bool:
        ...

    @staticmethod
    @overload
    def IsSortable(ch: str) -> bool:
        ...

    @staticmethod
    @overload
    def IsSortable(text: str) -> bool:
        ...

    @staticmethod
    @overload
    def IsSortable(text: System.ReadOnlySpan[str]) -> bool:
        """
        Indicates whether a specified Unicode string is sortable.
        
        :param text: A string of zero or more Unicode characters.
        :returns: true if  is non-empty and contains only sortable Unicode characters; otherwise, false.
        """
        ...

    @staticmethod
    @overload
    def IsSortable(value: System.Text.Rune) -> bool:
        """
        Indicates whether a specified Rune is sortable.
        
        :param value: A Unicode scalar value.
        :returns: true if  is a sortable Unicode scalar value; otherwise, false.
        """
        ...

    @overload
    def IsSuffix(self, source: str, suffix: str, options: System.Globalization.CompareOptions) -> bool:
        """
        Determines whether suffix is a suffix of string.  If suffix equals
        string.Empty, true is returned.
        """
        ...

    @overload
    def IsSuffix(self, source: System.ReadOnlySpan[str], suffix: System.ReadOnlySpan[str], options: System.Globalization.CompareOptions = ...) -> bool:
        """
        Determines whether a string ends with a specific suffix.
        
        :param source: The string to search within.
        :param suffix: The suffix to attempt to match at the end of .
        :param options: The CompareOptions to use during the match.
        :returns: true if  occurs at the end of ; otherwise, false.
        """
        ...

    @overload
    def IsSuffix(self, source: System.ReadOnlySpan[str], suffix: System.ReadOnlySpan[str], options: System.Globalization.CompareOptions, matchLength: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Determines whether a string ends with a specific suffix.
        
        :param source: The string to search within.
        :param suffix: The suffix to attempt to match at the end of .
        :param options: The CompareOptions to use during the match.
        :param matchLength: When this method returns, contains the number of characters of  that matched the desired suffix. This may be different than the length of  if a linguistic comparison is performed. Set to 0 if the suffix did not match.
        :returns: true if  occurs at the end of ; otherwise, false.
        """
        ...

    @overload
    def IsSuffix(self, source: str, suffix: str) -> bool:
        ...

    @overload
    def LastIndexOf(self, source: str, value: str) -> int:
        """
        Returns the last index where value is found in string.  The
        search starts from startIndex and ends at endIndex.  Returns -1 if
        the specified value is not found.  If value equals string.Empty,
        endIndex is returned.  Throws IndexOutOfRange if startIndex or
        endIndex is less than zero or greater than the length of string.
        Throws ArgumentException if value (as a string) is null.
        """
        ...

    @overload
    def LastIndexOf(self, source: str, value: str) -> int:
        ...

    @overload
    def LastIndexOf(self, source: str, value: str, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def LastIndexOf(self, source: str, value: str, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def LastIndexOf(self, source: str, value: str, startIndex: int) -> int:
        ...

    @overload
    def LastIndexOf(self, source: str, value: str, startIndex: int) -> int:
        ...

    @overload
    def LastIndexOf(self, source: str, value: str, startIndex: int, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def LastIndexOf(self, source: str, value: str, startIndex: int, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def LastIndexOf(self, source: str, value: str, startIndex: int, count: int) -> int:
        ...

    @overload
    def LastIndexOf(self, source: str, value: str, startIndex: int, count: int) -> int:
        ...

    @overload
    def LastIndexOf(self, source: str, value: str, startIndex: int, count: int, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def LastIndexOf(self, source: str, value: str, startIndex: int, count: int, options: System.Globalization.CompareOptions) -> int:
        ...

    @overload
    def LastIndexOf(self, source: System.ReadOnlySpan[str], value: System.ReadOnlySpan[str], options: System.Globalization.CompareOptions = ...) -> int:
        """
        Searches for the last occurrence of a substring within a source string.
        
        :param source: The string to search within.
        :param value: The substring to locate within .
        :param options: The CompareOptions to use during the search.
        :returns: The zero-based index into  where the substring  last appears; or -1 if  cannot be found within .
        """
        ...

    @overload
    def LastIndexOf(self, source: System.ReadOnlySpan[str], value: System.ReadOnlySpan[str], options: System.Globalization.CompareOptions, matchLength: typing.Optional[int]) -> typing.Union[int, int]:
        """
        Searches for the last occurrence of a substring within a source string.
        
        :param source: The string to search within.
        :param value: The substring to locate within .
        :param options: The CompareOptions to use during the search.
        :param matchLength: When this method returns, contains the number of characters of  that matched the desired value. This may be different than the length of  if a linguistic comparison is performed. Set to 0 if  is not found within .
        :returns: The zero-based index into  where the substring  last appears; or -1 if  cannot be found within .
        """
        ...

    @overload
    def LastIndexOf(self, source: System.ReadOnlySpan[str], value: System.Text.Rune, options: System.Globalization.CompareOptions = ...) -> int:
        """
        Searches for the last occurrence of a Rune within a source string.
        
        :param source: The string to search within.
        :param value: The Rune to locate within .
        :param options: The CompareOptions to use during the search.
        :returns: The zero-based index into  where  last appears; or -1 if  cannot be found within .
        """
        ...

    def ToString(self) -> str:
        ...


class HijriCalendar(System.Globalization.Calendar):
    """This class has no documentation."""

    HijriEra: int = 1

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def AlgorithmType(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CalendarAlgorithmType enum."""
        ...

    @property
    def DaysInYearBeforeMinSupportedYear(self) -> int:
        """This property is protected."""
        ...

    @property
    def HijriAdjustment(self) -> int:
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    @property
    def TwoDigitYearMax(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    def AddMonths(self, time: typing.Union[datetime.datetime, datetime.date], months: int) -> datetime.datetime:
        ...

    def AddYears(self, time: typing.Union[datetime.datetime, datetime.date], years: int) -> datetime.datetime:
        ...

    def GetDayOfMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDayOfWeek(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """:returns: This method returns the int value of a member of the System.DayOfWeek enum."""
        ...

    def GetDayOfYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDaysInMonth(self, year: int, month: int, era: int) -> int:
        ...

    def GetDaysInYear(self, year: int, era: int) -> int:
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetLeapMonth(self, year: int, era: int) -> int:
        ...

    def GetMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetMonthsInYear(self, year: int, era: int) -> int:
        ...

    def GetYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def IsLeapDay(self, year: int, month: int, day: int, era: int) -> bool:
        ...

    def IsLeapMonth(self, year: int, month: int, era: int) -> bool:
        ...

    def IsLeapYear(self, year: int, era: int) -> bool:
        ...

    def ToDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, era: int) -> datetime.datetime:
        ...

    def ToFourDigitYear(self, year: int) -> int:
        ...


class CharUnicodeInfo(System.Object):
    """
    This class implements a set of methods for retrieving character type
    information. Character type information is independent of culture
    and region.
    """

    @staticmethod
    @overload
    def GetDecimalDigitValue(ch: str) -> int:
        ...

    @staticmethod
    @overload
    def GetDecimalDigitValue(s: str, index: int) -> int:
        ...

    @staticmethod
    @overload
    def GetDigitValue(ch: str) -> int:
        ...

    @staticmethod
    @overload
    def GetDigitValue(s: str, index: int) -> int:
        ...

    @staticmethod
    @overload
    def GetNumericValue(ch: str) -> float:
        ...

    @staticmethod
    @overload
    def GetNumericValue(s: str, index: int) -> float:
        ...

    @staticmethod
    @overload
    def GetUnicodeCategory(ch: str) -> int:
        """:returns: This method returns the int value of a member of the System.Globalization.UnicodeCategory enum."""
        ...

    @staticmethod
    @overload
    def GetUnicodeCategory(codePoint: int) -> int:
        """:returns: This method returns the int value of a member of the System.Globalization.UnicodeCategory enum."""
        ...

    @staticmethod
    @overload
    def GetUnicodeCategory(s: str, index: int) -> int:
        """:returns: This method returns the int value of a member of the System.Globalization.UnicodeCategory enum."""
        ...


class IdnMapping(System.Object):
    """This class has no documentation."""

    @property
    def AllowUnassigned(self) -> bool:
        ...

    @property
    def UseStd3AsciiRules(self) -> bool:
        ...

    def __init__(self) -> None:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def GetAscii(self, unicode: str) -> str:
        ...

    @overload
    def GetAscii(self, unicode: str, index: int) -> str:
        ...

    @overload
    def GetAscii(self, unicode: str, index: int, count: int) -> str:
        ...

    def GetHashCode(self) -> int:
        ...

    @overload
    def GetUnicode(self, ascii: str) -> str:
        ...

    @overload
    def GetUnicode(self, ascii: str, index: int) -> str:
        ...

    @overload
    def GetUnicode(self, ascii: str, index: int, count: int) -> str:
        ...


class EastAsianLunisolarCalendar(System.Globalization.Calendar, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def AlgorithmType(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CalendarAlgorithmType enum."""
        ...

    @property
    def TwoDigitYearMax(self) -> int:
        ...

    def AddMonths(self, time: typing.Union[datetime.datetime, datetime.date], months: int) -> datetime.datetime:
        """
        Returns the DateTime resulting from adding the given number of
        months to the specified DateTime. The result is computed by incrementing
        (or decrementing) the year and month parts of the specified DateTime by
        value months, and, if required, adjusting the day part of the
        resulting date downwards to the last day of the resulting month in the
        resulting year. The time-of-day part of the result is the same as the
        time-of-day part of the specified DateTime.
        """
        ...

    def AddYears(self, time: typing.Union[datetime.datetime, datetime.date], years: int) -> datetime.datetime:
        ...

    def GetCelestialStem(self, sexagenaryYear: int) -> int:
        """
        Return the celestial year from the 60-year cycle.
        The returned value is from 1 ~ 10.
        """
        ...

    def GetDayOfMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the day-of-month part of the specified DateTime. The returned
        value is an integer between 1 and 29 or 30.
        """
        ...

    def GetDayOfWeek(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the day-of-week part of the specified DateTime. The returned value
        is an integer between 0 and 6, where 0 indicates Sunday, 1 indicates
        Monday, 2 indicates Tuesday, 3 indicates Wednesday, 4 indicates
        Thursday, 5 indicates Friday, and 6 indicates Saturday.
        
        :returns: This method returns the int value of a member of the System.DayOfWeek enum.
        """
        ...

    def GetDayOfYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the day-of-year part of the specified DateTime. The returned value
        is an integer between 1 and [354|355 |383|384].
        """
        ...

    def GetDaysInMonth(self, year: int, month: int, era: int) -> int:
        """
        Returns the number of days in the month given by the year and
        month arguments.
        """
        ...

    def GetDaysInYear(self, year: int, era: int) -> int:
        """Returns the number of days in the year given by the year argument for the current era."""
        ...

    def GetLeapMonth(self, year: int, era: int) -> int:
        """
        Returns  the leap month in a calendar year of the specified era. This method returns 0
        if this year is not a leap year.
        """
        ...

    def GetMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the month part of the specified DateTime.
        The returned value is an integer between 1 and 13.
        """
        ...

    def GetMonthsInYear(self, year: int, era: int) -> int:
        """Returns the number of months in the specified year and era."""
        ...

    def GetSexagenaryYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """Return the year number in the 60-year cycle."""
        ...

    def GetTerrestrialBranch(self, sexagenaryYear: int) -> int:
        """
        Return the Terrestial Branch from the 60-year cycle.
        The returned value is from 1 ~ 12.
        """
        ...

    def GetYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the year part of the specified DateTime.
        The returned value is an integer between 1 and MaxCalendarYear.
        """
        ...

    def IsLeapDay(self, year: int, month: int, day: int, era: int) -> bool:
        """
        Checks whether a given day in the specified era is a leap day.
        This method returns true if the date is a leap day, or false if not.
        """
        ...

    def IsLeapMonth(self, year: int, month: int, era: int) -> bool:
        """
        Checks whether a given month in the specified era is a leap month.
        This method returns true if month is a leap month, or false if not.
        """
        ...

    def IsLeapYear(self, year: int, era: int) -> bool:
        """
        Checks whether a given year in the specified era is a leap year.
        This method returns true if year is a leap year, or false if not.
        """
        ...

    def ToDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, era: int) -> datetime.datetime:
        """
        Returns the date and time converted to a DateTime value.
        Throws an exception if the n-tuple is invalid.
        """
        ...

    def ToFourDigitYear(self, year: int) -> int:
        ...


class TaiwanLunisolarCalendar(System.Globalization.EastAsianLunisolarCalendar):
    """This class has no documentation."""

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def DaysInYearBeforeMinSupportedYear(self) -> int:
        """This property is protected."""
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    def __init__(self) -> None:
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...


class TextInfo(System.Object, System.ICloneable, System.Runtime.Serialization.IDeserializationCallback):
    """
    This Class defines behaviors specific to a writing system.
    A writing system is the collection of scripts and orthographic rules
    required to represent a language as text.
    """

    @property
    def ANSICodePage(self) -> int:
        ...

    @property
    def OEMCodePage(self) -> int:
        ...

    @property
    def MacCodePage(self) -> int:
        ...

    @property
    def EBCDICCodePage(self) -> int:
        ...

    @property
    def LCID(self) -> int:
        ...

    @property
    def CultureName(self) -> str:
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def ListSeparator(self) -> str:
        """Returns the string used to separate items in a list."""
        ...

    @property
    def IsRightToLeft(self) -> bool:
        """
        Returns true if the dominant direction of text and UI such as the
        relative position of buttons and scroll bars
        """
        ...

    def Clone(self) -> System.Object:
        ...

    def Equals(self, obj: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    @staticmethod
    def ReadOnly(textInfo: System.Globalization.TextInfo) -> System.Globalization.TextInfo:
        """
        Create a cloned readonly instance or return the input one if it is
        readonly.
        """
        ...

    @overload
    def ToLower(self, c: str) -> str:
        """
        Converts the character or string to lower case.  Certain locales
        have different casing semantics from the file systems in Win32.
        """
        ...

    @overload
    def ToLower(self, str: str) -> str:
        ...

    def ToString(self) -> str:
        ...

    def ToTitleCase(self, str: str) -> str:
        """
        Titlecasing refers to a casing practice wherein the first letter of a word is an uppercase letter
        and the rest of the letters are lowercase.  The choice of which words to titlecase in headings
        and titles is dependent on language and local conventions.  For example, "The Merry Wives of Windor"
        is the appropriate titlecasing of that play's name in English, with the word "of" not titlecased.
        In German, however, the title is "Die lustigen Weiber von Windsor," and both "lustigen" and "von"
        are not titlecased.  In French even fewer words are titlecased: "Les joyeuses commeres de Windsor."
        
        Moreover, the determination of what actually constitutes a word is language dependent, and this can
        influence which letter or letters of a "word" are uppercased when titlecasing strings.  For example
        "l'arbre" is considered two words in French, whereas "can't" is considered one word in English.
        """
        ...

    @overload
    def ToUpper(self, c: str) -> str:
        """
        Converts the character or string to upper case.  Certain locales
        have different casing semantics from the file systems in Win32.
        """
        ...

    @overload
    def ToUpper(self, str: str) -> str:
        ...


class CultureNotFoundException(System.ArgumentException):
    """This class has no documentation."""

    @property
    def InvalidCultureId(self) -> typing.Optional[int]:
        ...

    @property
    def InvalidCultureName(self) -> str:
        ...

    @property
    def Message(self) -> str:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, paramName: str, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, innerException: System.Exception) -> None:
        ...

    @overload
    def __init__(self, paramName: str, invalidCultureName: str, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, invalidCultureName: str, innerException: System.Exception) -> None:
        ...

    @overload
    def __init__(self, message: str, invalidCultureId: int, innerException: System.Exception) -> None:
        ...

    @overload
    def __init__(self, paramName: str, invalidCultureId: int, message: str) -> None:
        ...

    @overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        This method is protected.
        
        Obsoletions.LegacyFormatterImplMessage
        """
        ...

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """Obsoletions.LegacyFormatterImplMessage"""
        warnings.warn("Obsoletions.LegacyFormatterImplMessage", DeprecationWarning)


class KoreanLunisolarCalendar(System.Globalization.EastAsianLunisolarCalendar):
    """This class has no documentation."""

    GregorianEra: int = 1

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def DaysInYearBeforeMinSupportedYear(self) -> int:
        """This property is protected."""
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    def __init__(self) -> None:
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...


class GlobalizationExtensions(System.Object):
    """This class has no documentation."""

    @staticmethod
    def GetStringComparer(compareInfo: System.Globalization.CompareInfo, options: System.Globalization.CompareOptions) -> System.StringComparer:
        ...


class GregorianCalendarTypes(System.Enum):
    """This class has no documentation."""

    Localized = ...

    USEnglish = ...

    MiddleEastFrench = ...

    Arabic = ...

    TransliteratedEnglish = ...

    TransliteratedFrench = ...


class NumberFormatInfo(System.Object, System.IFormatProvider, System.ICloneable):
    """This class has no documentation."""

    InvariantInfo: System.Globalization.NumberFormatInfo
    """
    Returns a default NumberFormatInfo that will be universally
    supported and constant irrespective of the current culture.
    Used by FromString methods.
    """

    @property
    def CurrencyDecimalDigits(self) -> int:
        ...

    @property
    def CurrencyDecimalSeparator(self) -> str:
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def CurrencyGroupSizes(self) -> typing.List[int]:
        ...

    @property
    def NumberGroupSizes(self) -> typing.List[int]:
        ...

    @property
    def PercentGroupSizes(self) -> typing.List[int]:
        ...

    @property
    def CurrencyGroupSeparator(self) -> str:
        ...

    @property
    def CurrencySymbol(self) -> str:
        ...

    CurrentInfo: System.Globalization.NumberFormatInfo
    """Returns the current culture's NumberFormatInfo. Used by Parse methods."""

    @property
    def NaNSymbol(self) -> str:
        ...

    @property
    def CurrencyNegativePattern(self) -> int:
        ...

    @property
    def NumberNegativePattern(self) -> int:
        ...

    @property
    def PercentPositivePattern(self) -> int:
        ...

    @property
    def PercentNegativePattern(self) -> int:
        ...

    @property
    def NegativeInfinitySymbol(self) -> str:
        ...

    @property
    def NegativeSign(self) -> str:
        ...

    @property
    def NumberDecimalDigits(self) -> int:
        ...

    @property
    def NumberDecimalSeparator(self) -> str:
        ...

    @property
    def NumberGroupSeparator(self) -> str:
        ...

    @property
    def CurrencyPositivePattern(self) -> int:
        ...

    @property
    def PositiveInfinitySymbol(self) -> str:
        ...

    @property
    def PositiveSign(self) -> str:
        ...

    @property
    def PercentDecimalDigits(self) -> int:
        ...

    @property
    def PercentDecimalSeparator(self) -> str:
        ...

    @property
    def PercentGroupSeparator(self) -> str:
        ...

    @property
    def PercentSymbol(self) -> str:
        ...

    @property
    def PerMilleSymbol(self) -> str:
        ...

    @property
    def NativeDigits(self) -> typing.List[str]:
        ...

    @property
    def DigitSubstitution(self) -> int:
        """This property contains the int value of a member of the System.Globalization.DigitShapes enum."""
        ...

    def __init__(self) -> None:
        ...

    def Clone(self) -> System.Object:
        ...

    def GetFormat(self, formatType: typing.Type) -> System.Object:
        ...

    @staticmethod
    def GetInstance(formatProvider: System.IFormatProvider) -> System.Globalization.NumberFormatInfo:
        ...

    @staticmethod
    def ReadOnly(nfi: System.Globalization.NumberFormatInfo) -> System.Globalization.NumberFormatInfo:
        ...


class DateTimeFormatInfo(System.Object, System.IFormatProvider, System.ICloneable):
    """This class has no documentation."""

    InvariantInfo: System.Globalization.DateTimeFormatInfo
    """
    Returns a default DateTimeFormatInfo that will be universally
    supported and constant irrespective of the current culture.
    """

    CurrentInfo: System.Globalization.DateTimeFormatInfo
    """Returns the current culture's DateTimeFormatInfo."""

    @property
    def AMDesignator(self) -> str:
        ...

    @property
    def Calendar(self) -> System.Globalization.Calendar:
        ...

    @property
    def DateSeparator(self) -> str:
        ...

    @property
    def FirstDayOfWeek(self) -> int:
        """This property contains the int value of a member of the System.DayOfWeek enum."""
        ...

    @property
    def CalendarWeekRule(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CalendarWeekRule enum."""
        ...

    @property
    def FullDateTimePattern(self) -> str:
        ...

    @property
    def LongDatePattern(self) -> str:
        """
        For our "patterns" arrays we have 2 variables, a string and a string[]
        The string[] contains the list of patterns, EXCEPT the default may not be included.
        The string contains the default pattern.
        When we initially construct our string[], we set the string to string[0]
        """
        ...

    @property
    def LongTimePattern(self) -> str:
        """
        For our "patterns" arrays we have 2 variables, a string and a string[]
        
        The string[] contains the list of patterns, EXCEPT the default may not be included.
        The string contains the default pattern.
        When we initially construct our string[], we set the string to string[0]
        """
        ...

    @property
    def MonthDayPattern(self) -> str:
        ...

    @property
    def PMDesignator(self) -> str:
        ...

    @property
    def RFC1123Pattern(self) -> str:
        ...

    @property
    def ShortDatePattern(self) -> str:
        """
        For our "patterns" arrays we have 2 variables, a string and a string[]
        
        The string[] contains the list of patterns, EXCEPT the default may not be included.
        The string contains the default pattern.
        When we initially construct our string[], we set the string to string[0]
        """
        ...

    @property
    def ShortTimePattern(self) -> str:
        """
        For our "patterns" arrays we have 2 variables, a string and a string[]
        
        The string[] contains the list of patterns, EXCEPT the default may not be included.
        The string contains the default pattern.
        When we initially construct our string[], we set the string to string[0]
        """
        ...

    @property
    def SortableDateTimePattern(self) -> str:
        ...

    @property
    def TimeSeparator(self) -> str:
        ...

    @property
    def UniversalSortableDateTimePattern(self) -> str:
        ...

    @property
    def YearMonthPattern(self) -> str:
        """
        For our "patterns" arrays we have 2 variables, a string and a string[]
        
        The string[] contains the list of patterns, EXCEPT the default may not be included.
        The string contains the default pattern.
        When we initially construct our string[], we set the string to string[0]
        """
        ...

    @property
    def AbbreviatedDayNames(self) -> typing.List[str]:
        ...

    @property
    def ShortestDayNames(self) -> typing.List[str]:
        """Returns the string array of the one-letter day of week names."""
        ...

    @property
    def DayNames(self) -> typing.List[str]:
        ...

    @property
    def AbbreviatedMonthNames(self) -> typing.List[str]:
        ...

    @property
    def MonthNames(self) -> typing.List[str]:
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def NativeCalendarName(self) -> str:
        """
        Return the native name for the calendar in DTFI.Calendar.  The native name is referred to
        the culture used to create the DTFI.  E.g. in the following example, the native language is Japanese.
        DateTimeFormatInfo dtfi = new CultureInfo("ja-JP", false).DateTimeFormat.Calendar = new JapaneseCalendar();
        String nativeName = dtfi.NativeCalendarName; // Get the Japanese name for the Japanese calendar.
        DateTimeFormatInfo dtfi = new CultureInfo("ja-JP", false).DateTimeFormat.Calendar = new GregorianCalendar(GregorianCalendarTypes.Localized);
        String nativeName = dtfi.NativeCalendarName; // Get the Japanese name for the Gregorian calendar.
        """
        ...

    @property
    def AbbreviatedMonthGenitiveNames(self) -> typing.List[str]:
        ...

    @property
    def MonthGenitiveNames(self) -> typing.List[str]:
        ...

    def __init__(self) -> None:
        ...

    def Clone(self) -> System.Object:
        ...

    def GetAbbreviatedDayName(self, dayofweek: System.DayOfWeek) -> str:
        ...

    def GetAbbreviatedEraName(self, era: int) -> str:
        ...

    def GetAbbreviatedMonthName(self, month: int) -> str:
        ...

    @overload
    def GetAllDateTimePatterns(self) -> typing.List[str]:
        ...

    @overload
    def GetAllDateTimePatterns(self, format: str) -> typing.List[str]:
        ...

    def GetDayName(self, dayofweek: System.DayOfWeek) -> str:
        ...

    def GetEra(self, eraName: str) -> int:
        """Get the era value by parsing the name of the era."""
        ...

    def GetEraName(self, era: int) -> str:
        """
        Get the name of the era for the specified era value.
        Era names are 1 indexed
        """
        ...

    def GetFormat(self, formatType: typing.Type) -> System.Object:
        ...

    @staticmethod
    def GetInstance(provider: System.IFormatProvider) -> System.Globalization.DateTimeFormatInfo:
        ...

    def GetMonthName(self, month: int) -> str:
        ...

    def GetShortestDayName(self, dayOfWeek: System.DayOfWeek) -> str:
        """Returns the super short day of week names for the specified day of week."""
        ...

    @staticmethod
    def ReadOnly(dtfi: System.Globalization.DateTimeFormatInfo) -> System.Globalization.DateTimeFormatInfo:
        ...

    def SetAllDateTimePatterns(self, patterns: typing.List[str], format: str) -> None:
        """
        Used by custom cultures and others to set the list of available formats. Note that none of them are
        explicitly used unless someone calls GetAllDateTimePatterns and subsequently uses one of the items
        from the list.
        
        Most of the format characters that can be used in GetAllDateTimePatterns are
        not really needed since they are one of the following:
        
         r/R/s/u     locale-independent constants -- cannot be changed!
         m/M/y/Y     fields with a single string in them -- that can be set through props directly
         f/F/g/G/U   derived fields based on combinations of various of the below formats
        
        NOTE: No special validation is done here beyond what is done when the actual respective fields
        are used (what would be the point of disallowing here what we allow in the appropriate property?)
        
        WARNING: If more validation is ever done in one place, it should be done in the other.
        """
        ...


class CultureTypes(System.Enum):
    """This class has no documentation."""

    NeutralCultures = ...

    SpecificCultures = ...

    InstalledWin32Cultures = ...

    AllCultures = ...

    UserCustomCulture = ...

    ReplacementCultures = ...

    WindowsOnlyCultures = ...
    """CultureTypes.WindowsOnlyCultures has been deprecated. Use other values in CultureTypes instead."""

    FrameworkCultures = ...
    """CultureTypes.FrameworkCultures has been deprecated. Use other values in CultureTypes instead."""


class CultureInfo(System.Object, System.IFormatProvider, System.ICloneable):
    """
    This class represents the software preferences of a particular culture
    or community. It includes information such as the language, writing
    system and a calendar used by the culture as well as methods for
    common operations such as printing dates and sorting strings.
    """

    CurrentCulture: System.Globalization.CultureInfo
    """
    This instance provides methods based on the current user settings.
    These settings are volatile and may change over the lifetime of the
    thread.
    """

    CurrentUICulture: System.Globalization.CultureInfo

    InstalledUICulture: System.Globalization.CultureInfo

    DefaultThreadCurrentCulture: System.Globalization.CultureInfo

    DefaultThreadCurrentUICulture: System.Globalization.CultureInfo

    InvariantCulture: System.Globalization.CultureInfo
    """
    This instance provides methods, for example for casing and sorting,
    that are independent of the system and current user settings.  It
    should be used only by processes such as some system services that
    require such invariant results (eg. file systems).  In general,
    the results are not linguistically correct and do not match any
    culture info.
    """

    @property
    def Parent(self) -> System.Globalization.CultureInfo:
        """Return the parent CultureInfo for the current instance."""
        ...

    @property
    def LCID(self) -> int:
        ...

    @property
    def KeyboardLayoutId(self) -> int:
        ...

    @property
    def Name(self) -> str:
        """
        Returns the full name of the CultureInfo. The name is in format like
        "en-US" This version does NOT include sort information in the name.
        """
        ...

    @property
    def IetfLanguageTag(self) -> str:
        ...

    @property
    def DisplayName(self) -> str:
        """
        Returns the full name of the CultureInfo in the localized language.
        For example, if the localized language of the runtime is Spanish and the CultureInfo is
        US English, "Ingles (Estados Unidos)" will be returned.
        """
        ...

    @property
    def NativeName(self) -> str:
        """
        Returns the full name of the CultureInfo in the native language.
        For example, if the CultureInfo is US English, "English
        (United States)" will be returned.
        """
        ...

    @property
    def EnglishName(self) -> str:
        """
        Returns the full name of the CultureInfo in English.
        For example, if the CultureInfo is US English, "English
        (United States)" will be returned.
        """
        ...

    @property
    def TwoLetterISOLanguageName(self) -> str:
        """ie: en"""
        ...

    @property
    def ThreeLetterISOLanguageName(self) -> str:
        """ie: eng"""
        ...

    @property
    def ThreeLetterWindowsLanguageName(self) -> str:
        """
        Returns the 3 letter windows language name for the current instance.  eg: "ENU"
        The ISO names are much preferred
        """
        ...

    @property
    def CompareInfo(self) -> System.Globalization.CompareInfo:
        """Gets the CompareInfo for this culture."""
        ...

    @property
    def TextInfo(self) -> System.Globalization.TextInfo:
        """Gets the TextInfo for this culture."""
        ...

    @property
    def IsNeutralCulture(self) -> bool:
        ...

    @property
    def CultureTypes(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CultureTypes enum."""
        ...

    @property
    def NumberFormat(self) -> System.Globalization.NumberFormatInfo:
        ...

    @property
    def DateTimeFormat(self) -> System.Globalization.DateTimeFormatInfo:
        """
        Create a DateTimeFormatInfo, and fill in the properties according to
        the CultureID.
        """
        ...

    @property
    def Calendar(self) -> System.Globalization.Calendar:
        """
        Return/set the default calendar used by this culture.
        This value can be overridden by regional option if this is a current culture.
        """
        ...

    @property
    def OptionalCalendars(self) -> typing.List[System.Globalization.Calendar]:
        """Return an array of the optional calendar for this culture."""
        ...

    @property
    def UseUserOverride(self) -> bool:
        ...

    @property
    def IsReadOnly(self) -> bool:
        ...

    @overload
    def __init__(self, name: str) -> None:
        ...

    @overload
    def __init__(self, name: str, useUserOverride: bool) -> None:
        ...

    @overload
    def __init__(self, culture: int) -> None:
        ...

    @overload
    def __init__(self, culture: int, useUserOverride: bool) -> None:
        ...

    def ClearCachedData(self) -> None:
        ...

    def Clone(self) -> System.Object:
        ...

    @staticmethod
    def CreateSpecificCulture(name: str) -> System.Globalization.CultureInfo:
        """
        Return a specific culture. A tad irrelevant now since we always
        return valid data for neutral locales.
        
        Note that there's interesting behavior that tries to find a
        smaller name, ala RFC4647, if we can't find a bigger name.
        That doesn't help with things like "zh" though, so the approach
        is of questionable value
        """
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetConsoleFallbackUICulture(self) -> System.Globalization.CultureInfo:
        ...

    @staticmethod
    @overload
    def GetCultureInfo(culture: int) -> System.Globalization.CultureInfo:
        """
        Gets a cached copy of the specified culture from an internal
        hashtable (or creates it if not found). (LCID version)
        """
        ...

    @staticmethod
    @overload
    def GetCultureInfo(name: str) -> System.Globalization.CultureInfo:
        """
        Gets a cached copy of the specified culture from an internal
        hashtable (or creates it if not found). (Named version)
        """
        ...

    @staticmethod
    @overload
    def GetCultureInfo(name: str, altName: str) -> System.Globalization.CultureInfo:
        """
        Gets a cached copy of the specified culture from an internal
        hashtable (or creates it if not found).
        """
        ...

    @staticmethod
    @overload
    def GetCultureInfo(name: str, predefinedOnly: bool) -> System.Globalization.CultureInfo:
        ...

    @staticmethod
    def GetCultureInfoByIetfLanguageTag(name: str) -> System.Globalization.CultureInfo:
        ...

    @staticmethod
    def GetCultures(types: System.Globalization.CultureTypes) -> typing.List[System.Globalization.CultureInfo]:
        ...

    def GetFormat(self, formatType: typing.Type) -> System.Object:
        ...

    def GetHashCode(self) -> int:
        ...

    @staticmethod
    def ReadOnly(ci: System.Globalization.CultureInfo) -> System.Globalization.CultureInfo:
        ...

    def ToString(self) -> str:
        """
        Implements object.ToString(). Returns the name of the CultureInfo,
        eg. "de-DE_phoneb", "en-US", or "fj-FJ".
        """
        ...


class TextElementEnumerator(System.Object, System.Collections.IEnumerator):
    """This class has no documentation."""

    @property
    def Current(self) -> System.Object:
        ...

    @property
    def ElementIndex(self) -> int:
        ...

    def GetTextElement(self) -> str:
        ...

    def MoveNext(self) -> bool:
        ...

    def Reset(self) -> None:
        ...


class StringInfo(System.Object):
    """
    This class defines behaviors specific to a writing system.
    A writing system is the collection of scripts and orthographic rules
    required to represent a language as text.
    """

    @property
    def String(self) -> str:
        ...

    @property
    def LengthInTextElements(self) -> int:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, value: str) -> None:
        ...

    def Equals(self, value: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    @staticmethod
    @overload
    def GetNextTextElement(str: str) -> str:
        """
        Returns the first text element (extended grapheme cluster) that occurs in the input string.
        
        :param str: The input string to analyze.
        :returns: The substring corresponding to the first text element within , or the empty string if  is empty.
        """
        ...

    @staticmethod
    @overload
    def GetNextTextElement(str: str, index: int) -> str:
        """
        Returns the first text element (extended grapheme cluster) that occurs in the input string
        starting at the specified index.
        
        :param str: The input string to analyze.
        :param index: The char offset in  at which to begin analysis.
        :returns: The substring corresponding to the first text element within  starting at index , or the empty string if  corresponds to the end of .
        """
        ...

    @staticmethod
    @overload
    def GetNextTextElementLength(str: str) -> int:
        """
        Returns the length of the first text element (extended grapheme cluster) that occurs in the input string.
        
        :param str: The input string to analyze.
        :returns: The length (in chars) of the substring corresponding to the first text element within , or 0 if  is empty.
        """
        ...

    @staticmethod
    @overload
    def GetNextTextElementLength(str: str, index: int) -> int:
        """
        Returns the length of the first text element (extended grapheme cluster) that occurs in the input string
        starting at the specified index.
        
        :param str: The input string to analyze.
        :param index: The char offset in  at which to begin analysis.
        :returns: The length (in chars) of the substring corresponding to the first text element within  starting at index , or 0 if  corresponds to the end of .
        """
        ...

    @staticmethod
    @overload
    def GetNextTextElementLength(str: System.ReadOnlySpan[str]) -> int:
        """
        Returns the length of the first text element (extended grapheme cluster) that occurs in the input span.
        
        :param str: The input span to analyze.
        :returns: The length (in chars) of the substring corresponding to the first text element within , or 0 if  is empty.
        """
        ...

    @staticmethod
    @overload
    def GetTextElementEnumerator(str: str) -> System.Globalization.TextElementEnumerator:
        ...

    @staticmethod
    @overload
    def GetTextElementEnumerator(str: str, index: int) -> System.Globalization.TextElementEnumerator:
        ...

    @staticmethod
    def ParseCombiningCharacters(str: str) -> typing.List[int]:
        """
        Returns the indices of each base character or properly formed surrogate
        pair  within the str. It recognizes a base character plus one or more
        combining characters or a properly formed surrogate pair as a text
        element and returns the index of the base character or high surrogate.
        Each index is the beginning of a text element within a str. The length
        of each element is easily computed as the difference between successive
        indices. The length of the array will always be less than or equal to
        the length of the str. For example, given the str
        \\u4f00\\u302a\\ud800\\udc00\\u4f01, this method would return the indices:
        0, 2, 4.
        """
        ...

    @overload
    def SubstringByTextElements(self, startingTextElement: int) -> str:
        ...

    @overload
    def SubstringByTextElements(self, startingTextElement: int, lengthInTextElements: int) -> str:
        ...


class CalendarAlgorithmType(System.Enum):
    """This class has no documentation."""

    Unknown = 0

    SolarCalendar = 1

    LunarCalendar = 2

    LunisolarCalendar = 3


class DaylightTime(System.Object):
    """This class has no documentation."""

    @property
    def Start(self) -> datetime.datetime:
        ...

    @property
    def End(self) -> datetime.datetime:
        ...

    @property
    def Delta(self) -> datetime.timedelta:
        ...

    def __init__(self, start: typing.Union[datetime.datetime, datetime.date], end: typing.Union[datetime.datetime, datetime.date], delta: datetime.timedelta) -> None:
        ...


class TimeSpanStyles(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = ...

    AssumeNegative = ...


class UmAlQuraCalendar(System.Globalization.Calendar):
    """This class has no documentation."""

    UmAlQuraEra: int = 1

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def AlgorithmType(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CalendarAlgorithmType enum."""
        ...

    @property
    def DaysInYearBeforeMinSupportedYear(self) -> int:
        """This property is protected."""
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    @property
    def TwoDigitYearMax(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    def AddMonths(self, time: typing.Union[datetime.datetime, datetime.date], months: int) -> datetime.datetime:
        ...

    def AddYears(self, time: typing.Union[datetime.datetime, datetime.date], years: int) -> datetime.datetime:
        ...

    def GetDayOfMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDayOfWeek(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """:returns: This method returns the int value of a member of the System.DayOfWeek enum."""
        ...

    def GetDayOfYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDaysInMonth(self, year: int, month: int, era: int) -> int:
        ...

    def GetDaysInYear(self, year: int, era: int) -> int:
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetLeapMonth(self, year: int, era: int) -> int:
        ...

    def GetMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetMonthsInYear(self, year: int, era: int) -> int:
        ...

    def GetYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def IsLeapDay(self, year: int, month: int, day: int, era: int) -> bool:
        ...

    def IsLeapMonth(self, year: int, month: int, era: int) -> bool:
        ...

    def IsLeapYear(self, year: int, era: int) -> bool:
        ...

    def ToDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, era: int) -> datetime.datetime:
        ...

    def ToFourDigitYear(self, year: int) -> int:
        ...


class KoreanCalendar(System.Globalization.Calendar):
    """
    Korean calendar is based on the Gregorian calendar.  And the year is an offset to Gregorian calendar.
    That is,
         Korean year = Gregorian year + 2333.  So 2000/01/01 A.D. is Korean 4333/01/01
    
    0001/1/1 A.D. is Korean year 2334.
    """

    KoreanEra: int = 1

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def AlgorithmType(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CalendarAlgorithmType enum."""
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    @property
    def TwoDigitYearMax(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    def AddMonths(self, time: typing.Union[datetime.datetime, datetime.date], months: int) -> datetime.datetime:
        ...

    def AddYears(self, time: typing.Union[datetime.datetime, datetime.date], years: int) -> datetime.datetime:
        ...

    def GetDayOfMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDayOfWeek(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """:returns: This method returns the int value of a member of the System.DayOfWeek enum."""
        ...

    def GetDayOfYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDaysInMonth(self, year: int, month: int, era: int) -> int:
        ...

    def GetDaysInYear(self, year: int, era: int) -> int:
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetLeapMonth(self, year: int, era: int) -> int:
        ...

    def GetMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetMonthsInYear(self, year: int, era: int) -> int:
        ...

    def GetWeekOfYear(self, time: typing.Union[datetime.datetime, datetime.date], rule: System.Globalization.CalendarWeekRule, firstDayOfWeek: System.DayOfWeek) -> int:
        ...

    def GetYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def IsLeapDay(self, year: int, month: int, day: int, era: int) -> bool:
        ...

    def IsLeapMonth(self, year: int, month: int, era: int) -> bool:
        ...

    def IsLeapYear(self, year: int, era: int) -> bool:
        ...

    def ToDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, era: int) -> datetime.datetime:
        ...

    def ToFourDigitYear(self, year: int) -> int:
        ...


class NumberStyles(System.Enum):
    """
    Contains valid formats for Numbers recognized by the Number
    class' parsing code.
    """

    # Cannot convert to Python: None = ...

    AllowLeadingWhite = ...
    """
    Bit flag indicating that leading whitespace is allowed. Character values
    0x0009, 0x000A, 0x000B, 0x000C, 0x000D, and 0x0020 are considered to be
    whitespace.
    """

    AllowTrailingWhite = ...
    """Bitflag indicating trailing whitespace is allowed."""

    AllowLeadingSign = ...
    """
    Can the number start with a sign char specified by
    NumberFormatInfo.PositiveSign and NumberFormatInfo.NegativeSign
    """

    AllowTrailingSign = ...
    """Allow the number to end with a sign char"""

    AllowParentheses = ...
    """Allow the number to be enclosed in parens"""

    AllowDecimalPoint = ...

    AllowThousands = ...

    AllowExponent = ...

    AllowCurrencySymbol = ...

    AllowHexSpecifier = ...

    AllowBinarySpecifier = ...
    """
    Indicates that the numeric string represents a binary value. Valid binary values include the numeric digits 0 and 1.
    Strings that are parsed using this style do not employ a prefix; "0b" cannot be used. A string that is parsed with
    the AllowBinarySpecifier style will always be interpreted as a binary value. The only flags that can
    be combined with AllowBinarySpecifier are AllowLeadingWhite and AllowTrailingWhite.
    The NumberStyles enumeration includes a composite style, BinaryNumber, that consists of
    these three flags.
    """

    Integer = ...

    HexNumber = ...

    BinaryNumber = ...
    """Indicates that the AllowLeadingWhite, AllowTrailingWhite, and AllowBinarySpecifier styles are used. This is a composite number style."""

    Number = ...

    Float = ...

    Currency = ...

    Any = ...


class DigitShapes(System.Enum):
    """This class has no documentation."""

    Context = ...

    # Cannot convert to Python: None = ...

    NativeNational = ...


class JapaneseCalendar(System.Globalization.Calendar):
    """
    JapaneseCalendar is based on Gregorian calendar.  The month and day values are the same as
    Gregorian calendar. However, the year value is an offset to the Gregorian
    year based on the era.
    
    This system is adopted by Emperor Meiji in 1868. The year value is counted based on the reign of an emperor,
    and the era begins on the day an emperor ascends the throne and continues until his death.
    The era changes at 12:00AM.
    
    For example, the current era is Reiwa. It started on 2019/5/1 A.D.  Therefore, Gregorian year 2019 is also Reiwa 1st.
    2019/5/1 A.D. is also Reiwa 1st 5/1.
    
    Any date in the year during which era is changed can be reckoned in either era. For example,
    2019/1/1 can be 1/1 Reiwa 1st year or 1/1 Heisei 31st year.
    
    Note:
     The DateTime can be represented by the JapaneseCalendar are limited to two factors:
         1. The min value and max value of DateTime class.
         2. The available era information.
    """

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def AlgorithmType(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CalendarAlgorithmType enum."""
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    @property
    def TwoDigitYearMax(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    def AddMonths(self, time: typing.Union[datetime.datetime, datetime.date], months: int) -> datetime.datetime:
        ...

    def AddYears(self, time: typing.Union[datetime.datetime, datetime.date], years: int) -> datetime.datetime:
        ...

    def GetDayOfMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDayOfWeek(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """:returns: This method returns the int value of a member of the System.DayOfWeek enum."""
        ...

    def GetDayOfYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDaysInMonth(self, year: int, month: int, era: int) -> int:
        ...

    def GetDaysInYear(self, year: int, era: int) -> int:
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetLeapMonth(self, year: int, era: int) -> int:
        ...

    def GetMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetMonthsInYear(self, year: int, era: int) -> int:
        ...

    def GetWeekOfYear(self, time: typing.Union[datetime.datetime, datetime.date], rule: System.Globalization.CalendarWeekRule, firstDayOfWeek: System.DayOfWeek) -> int:
        ...

    def GetYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def IsLeapDay(self, year: int, month: int, day: int, era: int) -> bool:
        ...

    def IsLeapMonth(self, year: int, month: int, era: int) -> bool:
        ...

    def IsLeapYear(self, year: int, era: int) -> bool:
        ...

    def ToDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, era: int) -> datetime.datetime:
        ...

    def ToFourDigitYear(self, year: int) -> int:
        """
        For Japanese calendar, four digit year is not used. Few emperors will live for more than one hundred years.
        Therefore, for any two digit number, we just return the original number.
        """
        ...


class ChineseLunisolarCalendar(System.Globalization.EastAsianLunisolarCalendar):
    """This class has no documentation."""

    ChineseEra: int = 1

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def DaysInYearBeforeMinSupportedYear(self) -> int:
        """This property is protected."""
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    def __init__(self) -> None:
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...


class TaiwanCalendar(System.Globalization.Calendar):
    """
    Taiwan calendar is based on the Gregorian calendar.  And the year is an offset to Gregorian calendar.
    That is,
         Taiwan year = Gregorian year - 1911.  So 1912/01/01 A.D. is Taiwan 1/01/01
    """

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def AlgorithmType(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CalendarAlgorithmType enum."""
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    @property
    def TwoDigitYearMax(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    def AddMonths(self, time: typing.Union[datetime.datetime, datetime.date], months: int) -> datetime.datetime:
        ...

    def AddYears(self, time: typing.Union[datetime.datetime, datetime.date], years: int) -> datetime.datetime:
        ...

    def GetDayOfMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDayOfWeek(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """:returns: This method returns the int value of a member of the System.DayOfWeek enum."""
        ...

    def GetDayOfYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDaysInMonth(self, year: int, month: int, era: int) -> int:
        ...

    def GetDaysInYear(self, year: int, era: int) -> int:
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetLeapMonth(self, year: int, era: int) -> int:
        ...

    def GetMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetMonthsInYear(self, year: int, era: int) -> int:
        ...

    def GetWeekOfYear(self, time: typing.Union[datetime.datetime, datetime.date], rule: System.Globalization.CalendarWeekRule, firstDayOfWeek: System.DayOfWeek) -> int:
        ...

    def GetYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def IsLeapDay(self, year: int, month: int, day: int, era: int) -> bool:
        ...

    def IsLeapMonth(self, year: int, month: int, era: int) -> bool:
        ...

    def IsLeapYear(self, year: int, era: int) -> bool:
        ...

    def ToDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, era: int) -> datetime.datetime:
        ...

    def ToFourDigitYear(self, year: int) -> int:
        """
        For Taiwan calendar, four digit year is not used.
        Therefore, for any two digit number, we just return the original number.
        """
        ...


class UnicodeCategory(System.Enum):
    """This class has no documentation."""

    UppercaseLetter = 0

    LowercaseLetter = 1

    TitlecaseLetter = 2

    ModifierLetter = 3

    OtherLetter = 4

    NonSpacingMark = 5

    SpacingCombiningMark = 6

    EnclosingMark = 7

    DecimalDigitNumber = 8

    LetterNumber = 9

    OtherNumber = 10

    SpaceSeparator = 11

    LineSeparator = 12

    ParagraphSeparator = 13

    Control = 14

    Format = 15

    Surrogate = 16

    PrivateUse = 17

    ConnectorPunctuation = 18

    DashPunctuation = 19

    OpenPunctuation = 20

    ClosePunctuation = 21

    InitialQuotePunctuation = 22

    FinalQuotePunctuation = 23

    OtherPunctuation = 24

    MathSymbol = 25

    CurrencySymbol = 26

    ModifierSymbol = 27

    OtherSymbol = 28

    OtherNotAssigned = 29


class JulianCalendar(System.Globalization.Calendar):
    """
    This class implements the Julian calendar. In 48 B.C. Julius Caesar
    ordered a calendar reform, and this calendar is called Julian calendar.
    It consisted of a solar year of twelve months and of 365 days with an
    extra day every fourth year.
    """

    JulianEra: int = 1

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def AlgorithmType(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CalendarAlgorithmType enum."""
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    @property
    def TwoDigitYearMax(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    def AddMonths(self, time: typing.Union[datetime.datetime, datetime.date], months: int) -> datetime.datetime:
        ...

    def AddYears(self, time: typing.Union[datetime.datetime, datetime.date], years: int) -> datetime.datetime:
        ...

    def GetDayOfMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDayOfWeek(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """:returns: This method returns the int value of a member of the System.DayOfWeek enum."""
        ...

    def GetDayOfYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDaysInMonth(self, year: int, month: int, era: int) -> int:
        ...

    def GetDaysInYear(self, year: int, era: int) -> int:
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetLeapMonth(self, year: int, era: int) -> int:
        ...

    def GetMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetMonthsInYear(self, year: int, era: int) -> int:
        ...

    def GetYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def IsLeapDay(self, year: int, month: int, day: int, era: int) -> bool:
        ...

    def IsLeapMonth(self, year: int, month: int, era: int) -> bool:
        ...

    def IsLeapYear(self, year: int, era: int) -> bool:
        ...

    def ToDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, era: int) -> datetime.datetime:
        ...

    def ToFourDigitYear(self, year: int) -> int:
        ...


class PersianCalendar(System.Globalization.Calendar):
    """
    Modern Persian calendar is a solar observation based calendar. Each new year begins on the day when the vernal equinox occurs before noon.
    The epoch is the date of the vernal equinox prior to the epoch of the Islamic calendar (March 19, 622 Julian or March 22, 622 Gregorian)
    There is no Persian year 0. Ordinary years have 365 days. Leap years have 366 days with the last month (Esfand) gaining the extra day.
    """

    PersianEra: int = 1

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def AlgorithmType(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CalendarAlgorithmType enum."""
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    @property
    def TwoDigitYearMax(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    def AddMonths(self, time: typing.Union[datetime.datetime, datetime.date], months: int) -> datetime.datetime:
        ...

    def AddYears(self, time: typing.Union[datetime.datetime, datetime.date], years: int) -> datetime.datetime:
        ...

    def GetDayOfMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDayOfWeek(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """:returns: This method returns the int value of a member of the System.DayOfWeek enum."""
        ...

    def GetDayOfYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDaysInMonth(self, year: int, month: int, era: int) -> int:
        ...

    def GetDaysInYear(self, year: int, era: int) -> int:
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetLeapMonth(self, year: int, era: int) -> int:
        ...

    def GetMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetMonthsInYear(self, year: int, era: int) -> int:
        ...

    def GetYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def IsLeapDay(self, year: int, month: int, day: int, era: int) -> bool:
        ...

    def IsLeapMonth(self, year: int, month: int, era: int) -> bool:
        ...

    def IsLeapYear(self, year: int, era: int) -> bool:
        ...

    def ToDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, era: int) -> datetime.datetime:
        ...

    def ToFourDigitYear(self, year: int) -> int:
        ...


class ISOWeek(System.Object):
    """This class has no documentation."""

    @staticmethod
    def GetWeekOfYear(date: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    @staticmethod
    def GetWeeksInYear(year: int) -> int:
        ...

    @staticmethod
    def GetYear(date: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    @staticmethod
    def GetYearEnd(year: int) -> datetime.datetime:
        ...

    @staticmethod
    def GetYearStart(year: int) -> datetime.datetime:
        ...

    @staticmethod
    def ToDateTime(year: int, week: int, dayOfWeek: System.DayOfWeek) -> datetime.datetime:
        ...


class GregorianCalendar(System.Globalization.Calendar):
    """This class has no documentation."""

    ADEra: int = 1

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def AlgorithmType(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CalendarAlgorithmType enum."""
        ...

    @property
    def CalendarType(self) -> int:
        """This property contains the int value of a member of the System.Globalization.GregorianCalendarTypes enum."""
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    @property
    def TwoDigitYearMax(self) -> int:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, type: System.Globalization.GregorianCalendarTypes) -> None:
        ...

    def AddMonths(self, time: typing.Union[datetime.datetime, datetime.date], months: int) -> datetime.datetime:
        """
        Returns the DateTime resulting from adding the given number of
        months to the specified DateTime. The result is computed by incrementing
        (or decrementing) the year and month parts of the specified DateTime by
        value months, and, if required, adjusting the day part of the
        resulting date downwards to the last day of the resulting month in the
        resulting year. The time-of-day part of the result is the same as the
        time-of-day part of the specified DateTime.
        
        In more precise terms, considering the specified DateTime to be of the
        form y / m / d + t, where y is the
        year, m is the month, d is the day, and t is the
        time-of-day, the result is y1 / m1 / d1 + t,
        where y1 and m1 are computed by adding value months
        to y and m, and d1 is the largest value less than
        or equal to d that denotes a valid day in month m1 of year
        y1.
        """
        ...

    def AddYears(self, time: typing.Union[datetime.datetime, datetime.date], years: int) -> datetime.datetime:
        """
        Returns the DateTime resulting from adding the given number of
        years to the specified DateTime. The result is computed by incrementing
        (or decrementing) the year part of the specified DateTime by value
        years. If the month and day of the specified DateTime is 2/29, and if the
        resulting year is not a leap year, the month and day of the resulting
        DateTime becomes 2/28. Otherwise, the month, day, and time-of-day
        parts of the result are the same as those of the specified DateTime.
        """
        ...

    def GetDayOfMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the day-of-month part of the specified DateTime. The returned
        value is an integer between 1 and 31.
        """
        ...

    def GetDayOfWeek(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the day-of-week part of the specified DateTime. The returned value
        is an integer between 0 and 6, where 0 indicates Sunday, 1 indicates
        Monday, 2 indicates Tuesday, 3 indicates Wednesday, 4 indicates
        Thursday, 5 indicates Friday, and 6 indicates Saturday.
        
        :returns: This method returns the int value of a member of the System.DayOfWeek enum.
        """
        ...

    def GetDayOfYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the day-of-year part of the specified DateTime. The returned value
        is an integer between 1 and 366.
        """
        ...

    def GetDaysInMonth(self, year: int, month: int, era: int) -> int:
        """
        Returns the number of days in the month given by the year and
        month arguments.
        """
        ...

    def GetDaysInYear(self, year: int, era: int) -> int:
        """
        Returns the number of days in the year given by the year argument for
        the current era.
        """
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetLeapMonth(self, year: int, era: int) -> int:
        """
        Returns the leap month in a calendar year of the specified era.
        This method returns 0 if this calendar does not have leap month, or
        this year is not a leap year.
        """
        ...

    def GetMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the month part of the specified DateTime.
        The returned value is an integer between 1 and 12.
        """
        ...

    def GetMonthsInYear(self, year: int, era: int) -> int:
        """Returns the number of months in the specified year and era."""
        ...

    def GetYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """
        Returns the year part of the specified DateTime. The returned value is an
        integer between 1 and 9999.
        """
        ...

    def IsLeapDay(self, year: int, month: int, day: int, era: int) -> bool:
        """
        Checks whether a given day in the specified era is a leap day. This method returns true if
        the date is a leap day, or false if not.
        """
        ...

    def IsLeapMonth(self, year: int, month: int, era: int) -> bool:
        """
        Checks whether a given month in the specified era is a leap month.
        This method returns true if month is a leap month, or false if not.
        """
        ...

    def IsLeapYear(self, year: int, era: int) -> bool:
        """
        Checks whether a given year in the specified era is a leap year. This method returns true if
        year is a leap year, or false if not.
        """
        ...

    def ToDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, era: int) -> datetime.datetime:
        """
        Returns the date and time converted to a DateTime value.
        Throws an exception if the n-tuple is invalid.
        """
        ...

    def ToFourDigitYear(self, year: int) -> int:
        ...


class HebrewCalendar(System.Globalization.Calendar):
    """This class has no documentation."""

    HebrewEra: int = 1

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def AlgorithmType(self) -> int:
        """This property contains the int value of a member of the System.Globalization.CalendarAlgorithmType enum."""
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    @property
    def TwoDigitYearMax(self) -> int:
        ...

    def __init__(self) -> None:
        ...

    def AddMonths(self, time: typing.Union[datetime.datetime, datetime.date], months: int) -> datetime.datetime:
        ...

    def AddYears(self, time: typing.Union[datetime.datetime, datetime.date], years: int) -> datetime.datetime:
        ...

    def GetDayOfMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDayOfWeek(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        """:returns: This method returns the int value of a member of the System.DayOfWeek enum."""
        ...

    def GetDayOfYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetDaysInMonth(self, year: int, month: int, era: int) -> int:
        ...

    def GetDaysInYear(self, year: int, era: int) -> int:
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetLeapMonth(self, year: int, era: int) -> int:
        ...

    def GetMonth(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def GetMonthsInYear(self, year: int, era: int) -> int:
        ...

    def GetYear(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...

    def IsLeapDay(self, year: int, month: int, day: int, era: int) -> bool:
        ...

    def IsLeapMonth(self, year: int, month: int, era: int) -> bool:
        ...

    def IsLeapYear(self, year: int, era: int) -> bool:
        ...

    def ToDateTime(self, year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, era: int) -> datetime.datetime:
        ...

    def ToFourDigitYear(self, year: int) -> int:
        ...


class RegionInfo(System.Object):
    """
    This class represents settings specified by de jure or de facto
    standards for a particular country/region. In contrast to
    CultureInfo, the RegionInfo does not represent preferences of the
    user and does not depend on the user's language or culture.
    """

    CurrentRegion: System.Globalization.RegionInfo
    """
    This instance provides methods based on the current user settings.
    These settings are volatile and may change over the lifetime of the
    """

    @property
    def Name(self) -> str:
        """Returns the name of the region (ie: en-US)"""
        ...

    @property
    def EnglishName(self) -> str:
        """Returns the name of the region in English. (ie: United States)"""
        ...

    @property
    def DisplayName(self) -> str:
        """
        Returns the display name (localized) of the region. (ie: United States
        if the current UI language is en-US)
        """
        ...

    @property
    def NativeName(self) -> str:
        """
        Returns the native name of the region. (ie: Deutschland)
         WARNING: You need a full locale name for this to make sense.
        """
        ...

    @property
    def TwoLetterISORegionName(self) -> str:
        """Returns the two letter ISO region name (ie: US)"""
        ...

    @property
    def ThreeLetterISORegionName(self) -> str:
        """Returns the three letter ISO region name (ie: USA)"""
        ...

    @property
    def ThreeLetterWindowsRegionName(self) -> str:
        """Returns the three letter windows region name (ie: USA)"""
        ...

    @property
    def IsMetric(self) -> bool:
        """Returns true if this region uses the metric measurement system"""
        ...

    @property
    def GeoId(self) -> int:
        ...

    @property
    def CurrencyEnglishName(self) -> str:
        """English name for this region's currency, ie: Swiss Franc"""
        ...

    @property
    def CurrencyNativeName(self) -> str:
        """
        Native name for this region's currency, ie: Schweizer Franken
        WARNING: You need a full locale name for this to make sense.
        """
        ...

    @property
    def CurrencySymbol(self) -> str:
        """Currency Symbol for this locale, ie: Fr. or $"""
        ...

    @property
    def ISOCurrencySymbol(self) -> str:
        """ISO Currency Symbol for this locale, ie: CHF"""
        ...

    @overload
    def __init__(self, name: str) -> None:
        ...

    @overload
    def __init__(self, culture: int) -> None:
        ...

    def Equals(self, value: typing.Any) -> bool:
        """
        Implements Object.Equals().  Returns a boolean indicating whether
        or not object refers to the same RegionInfo as the current instance.
        RegionInfos are considered equal if and only if they have the same name
        (ie: en-US)
        """
        ...

    def GetHashCode(self) -> int:
        ...

    def ToString(self) -> str:
        ...


class JapaneseLunisolarCalendar(System.Globalization.EastAsianLunisolarCalendar):
    """This class has no documentation."""

    JapaneseEra: int = 1

    @property
    def MinSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def MaxSupportedDateTime(self) -> datetime.datetime:
        ...

    @property
    def DaysInYearBeforeMinSupportedYear(self) -> int:
        """This property is protected."""
        ...

    @property
    def Eras(self) -> typing.List[int]:
        ...

    def __init__(self) -> None:
        ...

    def GetEra(self, time: typing.Union[datetime.datetime, datetime.date]) -> int:
        ...


class DateTimeStyles(System.Enum):
    """Defines the formatting options that customize string parsing for some date and time parsing methods."""

    # Cannot convert to Python: None = ...

    AllowLeadingWhite = ...

    AllowTrailingWhite = ...

    AllowInnerWhite = ...

    AllowWhiteSpaces = ...

    NoCurrentDateDefault = ...

    AdjustToUniversal = ...

    AssumeLocal = ...

    AssumeUniversal = ...

    RoundtripKind = ...


