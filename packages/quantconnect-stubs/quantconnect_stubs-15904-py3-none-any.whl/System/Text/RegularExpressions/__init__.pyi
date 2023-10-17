from typing import overload
import abc
import datetime
import typing
import warnings

import System
import System.Collections
import System.Collections.Generic
import System.Reflection
import System.Reflection.Emit
import System.Runtime.Serialization
import System.Text.RegularExpressions


class Capture(System.Object):
    """
    Represents the results from a single subexpression capture. The object represents
    one substring for a single successful capture.
    """

    @property
    def Index(self) -> int:
        """Returns the position in the original string where the first character of captured substring was found."""
        ...

    @property
    def Length(self) -> int:
        """Returns the length of the captured substring."""
        ...

    @property
    def Value(self) -> str:
        """Gets the captured substring from the input string."""
        ...

    @property
    def ValueSpan(self) -> System.ReadOnlySpan[str]:
        """Gets the captured span from the input string."""
        ...

    def ToString(self) -> str:
        """Returns the substring that was matched."""
        ...


class CaptureCollection(System.Object, System.Collections.Generic.IList[System.Text.RegularExpressions.Capture], System.Collections.Generic.IReadOnlyList[System.Text.RegularExpressions.Capture], System.Collections.IList, typing.Iterable[System.Text.RegularExpressions.Capture]):
    """
    Represents a sequence of capture substrings. The object is used
    to return the set of captures done by a single capturing group.
    """

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def Count(self) -> int:
        """Returns the number of captures."""
        ...

    @property
    def IsSynchronized(self) -> bool:
        ...

    @property
    def SyncRoot(self) -> System.Object:
        ...

    def __getitem__(self, i: int) -> System.Text.RegularExpressions.Capture:
        """Returns a specific capture, by index, in this collection."""
        ...

    @overload
    def CopyTo(self, array: System.Array, arrayIndex: int) -> None:
        ...

    @overload
    def CopyTo(self, array: typing.List[System.Text.RegularExpressions.Capture], arrayIndex: int) -> None:
        ...

    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """Provides an enumerator in the same order as Item[]."""
        ...


class Group(System.Text.RegularExpressions.Capture):
    """
    Represents the results from a single capturing group. A capturing group can
    capture zero, one, or more strings in a single match because of quantifiers, so
    Group supplies a collection of Capture objects.
    """

    @property
    def Success(self) -> bool:
        """Indicates whether the match is successful."""
        ...

    @property
    def Name(self) -> str:
        ...

    @property
    def Captures(self) -> System.Text.RegularExpressions.CaptureCollection:
        """
        Returns a collection of all the captures matched by the capturing
        group, in innermost-leftmost-first order (or innermost-rightmost-first order if
        compiled with the "r" option). The collection may have zero or more items.
        """
        ...

    @staticmethod
    def Synchronized(inner: System.Text.RegularExpressions.Group) -> System.Text.RegularExpressions.Group:
        """Returns a Group object equivalent to the one supplied that is safe to share between multiple threads."""
        ...


class GroupCollection(System.Object, System.Collections.Generic.IList[System.Text.RegularExpressions.Group], System.Collections.Generic.IReadOnlyList[System.Text.RegularExpressions.Group], System.Collections.IList, System.Collections.Generic.IReadOnlyDictionary[str, System.Text.RegularExpressions.Group], typing.Iterable[System.Text.RegularExpressions.Group]):
    """
    Represents a sequence of capture substrings. The object is used
    to return the set of captures done by a single capturing group.
    """

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def Count(self) -> int:
        """Returns the number of groups."""
        ...

    @property
    def IsSynchronized(self) -> bool:
        ...

    @property
    def SyncRoot(self) -> System.Object:
        ...

    @property
    def Keys(self) -> System.Collections.Generic.IEnumerable[str]:
        ...

    @property
    def Values(self) -> System.Collections.Generic.IEnumerable[System.Text.RegularExpressions.Group]:
        ...

    @overload
    def __getitem__(self, groupnum: int) -> System.Text.RegularExpressions.Group:
        ...

    @overload
    def __getitem__(self, groupname: str) -> System.Text.RegularExpressions.Group:
        ...

    def ContainsKey(self, key: str) -> bool:
        ...

    @overload
    def CopyTo(self, array: System.Array, arrayIndex: int) -> None:
        ...

    @overload
    def CopyTo(self, array: typing.List[System.Text.RegularExpressions.Group], arrayIndex: int) -> None:
        ...

    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """Provides an enumerator in the same order as Item[]."""
        ...

    def TryGetValue(self, key: str, value: typing.Optional[System.Text.RegularExpressions.Group]) -> typing.Union[bool, System.Text.RegularExpressions.Group]:
        ...


class Match(System.Text.RegularExpressions.Group):
    """Represents the results from a single regular expression match."""

    Empty: System.Text.RegularExpressions.Match
    """Returns an empty Match object."""

    @property
    def Groups(self) -> System.Text.RegularExpressions.GroupCollection:
        ...

    def NextMatch(self) -> System.Text.RegularExpressions.Match:
        """
        Returns a new Match with the results for the next match, starting
        at the position at which the last match ended (at the character beyond the last
        matched character).
        """
        ...

    def Result(self, replacement: str) -> str:
        """
        Returns the expansion of the passed replacement pattern. For
        example, if the replacement pattern is ?$1$2?, Result returns the concatenation
        of Group(1).ToString() and Group(2).ToString().
        """
        ...

    @staticmethod
    def Synchronized(inner: System.Text.RegularExpressions.Match) -> System.Text.RegularExpressions.Match:
        """
        Returns a Match instance equivalent to the one supplied that is safe to share
        between multiple threads.
        """
        ...


class MatchCollection(System.Object, System.Collections.Generic.IList[System.Text.RegularExpressions.Match], System.Collections.Generic.IReadOnlyList[System.Text.RegularExpressions.Match], System.Collections.IList, typing.Iterable[System.Text.RegularExpressions.Match]):
    """
    Represents the set of names appearing as capturing group
    names in a regular expression.
    """

    @property
    def IsReadOnly(self) -> bool:
        ...

    @property
    def Count(self) -> int:
        """Returns the number of captures."""
        ...

    @property
    def IsSynchronized(self) -> bool:
        ...

    @property
    def SyncRoot(self) -> System.Object:
        ...

    def __getitem__(self, i: int) -> System.Text.RegularExpressions.Match:
        """Returns the ith Match in the collection."""
        ...

    @overload
    def CopyTo(self, array: System.Array, arrayIndex: int) -> None:
        ...

    @overload
    def CopyTo(self, array: typing.List[System.Text.RegularExpressions.Match], arrayIndex: int) -> None:
        ...

    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """Provides an enumerator in the same order as Item[i]."""
        ...


class RegexCompilationInfo(System.Object):
    """Obsoletions.RegexCompileToAssemblyMessage"""

    @property
    def IsPublic(self) -> bool:
        ...

    @property
    def MatchTimeout(self) -> datetime.timedelta:
        ...

    @property
    def Name(self) -> str:
        ...

    @property
    def Namespace(self) -> str:
        ...

    @property
    def Options(self) -> System.Text.RegularExpressions.RegexOptions:
        ...

    @property
    def Pattern(self) -> str:
        ...

    @overload
    def __init__(self, pattern: str, options: System.Text.RegularExpressions.RegexOptions, name: str, fullnamespace: str, ispublic: bool) -> None:
        ...

    @overload
    def __init__(self, pattern: str, options: System.Text.RegularExpressions.RegexOptions, name: str, fullnamespace: str, ispublic: bool, matchTimeout: datetime.timedelta) -> None:
        ...


class ValueMatch:
    """Represents the results from a single regular expression match."""

    @property
    def Index(self) -> int:
        """Gets the position in the original span where the first character of the captured sliced span is found."""
        ...

    @property
    def Length(self) -> int:
        """Gets the length of the captured sliced span."""
        ...


class Regex(System.Object, System.Runtime.Serialization.ISerializable):
    """
    Represents an immutable regular expression. Also contains static methods that
    allow use of regular expressions without instantiating a Regex explicitly.
    """

    class ValueMatchEnumerator:
        """Represents an enumerator containing the set of successful matches found by iteratively applying a regular expression pattern to the input span."""

        @property
        def Current(self) -> System.Text.RegularExpressions.ValueMatch:
            """Gets the ValueMatch element at the current position of the enumerator."""
            ...

        def GetEnumerator(self) -> System.Text.RegularExpressions.Regex.ValueMatchEnumerator:
            """
            Provides an enumerator that iterates through the matches in the input span.
            
            :returns: A copy of this enumerator.
            """
            ...

        def MoveNext(self) -> bool:
            """
            Advances the enumerator to the next match in the span.
            
            :returns: true if the enumerator was successfully advanced to the next element; false if the enumerator cannot find additional matches.
            """
            ...

    @property
    def Caps(self) -> System.Collections.IDictionary:
        """This property is protected."""
        ...

    @property
    def CapNames(self) -> System.Collections.IDictionary:
        """This property is protected."""
        ...

    @property
    def Options(self) -> System.Text.RegularExpressions.RegexOptions:
        """Returns the options passed into the constructor"""
        ...

    @property
    def RightToLeft(self) -> bool:
        """Indicates whether the regular expression matches from right to left."""
        ...

    InfiniteMatchTimeout: datetime.timedelta = ...

    @property
    def MatchTimeout(self) -> datetime.timedelta:
        """Gets the timeout interval of the current instance."""
        ...

    CacheSize: int

    @overload
    def __init__(self) -> None:
        """This method is protected."""
        ...

    @overload
    def __init__(self, pattern: str) -> None:
        """Creates a regular expression object for the specified regular expression."""
        ...

    @overload
    def __init__(self, pattern: str, options: System.Text.RegularExpressions.RegexOptions) -> None:
        """Creates a regular expression object for the specified regular expression, with options that modify the pattern."""
        ...

    @overload
    def __init__(self, pattern: str, options: System.Text.RegularExpressions.RegexOptions, matchTimeout: datetime.timedelta) -> None:
        ...

    @overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        This method is protected.
        
        Obsoletions.LegacyFormatterImplMessage
        """
        ...

    @staticmethod
    @overload
    def CompileToAssembly(regexinfos: typing.List[System.Text.RegularExpressions.RegexCompilationInfo], assemblyname: System.Reflection.AssemblyName) -> None:
        """Obsoletions.RegexCompileToAssemblyMessage"""
        ...

    @staticmethod
    @overload
    def CompileToAssembly(regexinfos: typing.List[System.Text.RegularExpressions.RegexCompilationInfo], assemblyname: System.Reflection.AssemblyName, attributes: typing.List[System.Reflection.Emit.CustomAttributeBuilder]) -> None:
        """Obsoletions.RegexCompileToAssemblyMessage"""
        ...

    @staticmethod
    @overload
    def CompileToAssembly(regexinfos: typing.List[System.Text.RegularExpressions.RegexCompilationInfo], assemblyname: System.Reflection.AssemblyName, attributes: typing.List[System.Reflection.Emit.CustomAttributeBuilder], resourceFile: str) -> None:
        """Obsoletions.RegexCompileToAssemblyMessage"""
        ...

    @overload
    def Count(self, input: str) -> int:
        """
        Searches an input string for all occurrences of a regular expression and returns the number of matches.
        
        :param input: The string to search for a match.
        :returns: The number of matches.
        """
        ...

    @overload
    def Count(self, input: System.ReadOnlySpan[str]) -> int:
        """
        Searches an input span for all occurrences of a regular expression and returns the number of matches.
        
        :param input: The span to search for a match.
        :returns: The number of matches.
        """
        ...

    @overload
    def Count(self, input: System.ReadOnlySpan[str], startat: int) -> int:
        """
        Searches an input span for all occurrences of a regular expression and returns the number of matches.
        
        :param input: The span to search for a match.
        :param startat: The zero-based character position at which to start the search.
        :returns: The number of matches.
        """
        ...

    @staticmethod
    @overload
    def Count(input: str, pattern: str) -> int:
        """
        Searches an input string for all occurrences of a regular expression and returns the number of matches.
        
        :param input: The string to search for a match.
        :param pattern: The regular expression pattern to match.
        :returns: The number of matches.
        """
        ...

    @staticmethod
    @overload
    def Count(input: str, pattern: str, options: System.Text.RegularExpressions.RegexOptions) -> int:
        """
        Searches an input string for all occurrences of a regular expression and returns the number of matches.
        
        :param input: The string to search for a match.
        :param pattern: The regular expression pattern to match.
        :param options: A bitwise combination of the enumeration values that specify options for matching.
        :returns: The number of matches.
        """
        ...

    @staticmethod
    @overload
    def Count(input: str, pattern: str, options: System.Text.RegularExpressions.RegexOptions, matchTimeout: datetime.timedelta) -> int:
        """
        Searches an input string for all occurrences of a regular expression and returns the number of matches.
        
        :param input: The string to search for a match.
        :param pattern: The regular expression pattern to match.
        :param options: A bitwise combination of the enumeration values that specify options for matching.
        :param matchTimeout: A time-out interval, or InfiniteMatchTimeout to indicate that the method should not time out.
        :returns: The number of matches.
        """
        ...

    @staticmethod
    @overload
    def Count(input: System.ReadOnlySpan[str], pattern: str) -> int:
        """
        Searches an input span for all occurrences of a regular expression and returns the number of matches.
        
        :param input: The span to search for a match.
        :param pattern: The regular expression pattern to match.
        :returns: The number of matches.
        """
        ...

    @staticmethod
    @overload
    def Count(input: System.ReadOnlySpan[str], pattern: str, options: System.Text.RegularExpressions.RegexOptions) -> int:
        """
        Searches an input span for all occurrences of a regular expression and returns the number of matches.
        
        :param input: The span to search for a match.
        :param pattern: The regular expression pattern to match.
        :param options: A bitwise combination of the enumeration values that specify options for matching.
        :returns: The number of matches.
        """
        ...

    @staticmethod
    @overload
    def Count(input: System.ReadOnlySpan[str], pattern: str, options: System.Text.RegularExpressions.RegexOptions, matchTimeout: datetime.timedelta) -> int:
        """
        Searches an input span for all occurrences of a regular expression and returns the number of matches.
        
        :param input: The span to search for a match.
        :param pattern: The regular expression pattern to match.
        :param options: A bitwise combination of the enumeration values that specify options for matching.
        :param matchTimeout: A time-out interval, or InfiniteMatchTimeout to indicate that the method should not time out.
        :returns: The number of matches.
        """
        ...

    @staticmethod
    @overload
    def EnumerateMatches(input: System.ReadOnlySpan[str], pattern: str) -> System.Text.RegularExpressions.Regex.ValueMatchEnumerator:
        """
        Searches an input span for all occurrences of a regular expression and returns a ValueMatchEnumerator to iterate over the matches.
        
        :param input: The span to search for a match.
        :param pattern: The regular expression pattern to match.
        :returns: A ValueMatchEnumerator to iterate over the matches.
        """
        ...

    @staticmethod
    @overload
    def EnumerateMatches(input: System.ReadOnlySpan[str], pattern: str, options: System.Text.RegularExpressions.RegexOptions) -> System.Text.RegularExpressions.Regex.ValueMatchEnumerator:
        """
        Searches an input span for all occurrences of a regular expression and returns a ValueMatchEnumerator to iterate over the matches.
        
        :param input: The span to search for a match.
        :param pattern: The regular expression pattern to match.
        :param options: A bitwise combination of the enumeration values that specify options for matching.
        :returns: A ValueMatchEnumerator to iterate over the matches.
        """
        ...

    @staticmethod
    @overload
    def EnumerateMatches(input: System.ReadOnlySpan[str], pattern: str, options: System.Text.RegularExpressions.RegexOptions, matchTimeout: datetime.timedelta) -> System.Text.RegularExpressions.Regex.ValueMatchEnumerator:
        """
        Searches an input span for all occurrences of a regular expression and returns a ValueMatchEnumerator to iterate over the matches.
        
        :param input: The span to search for a match.
        :param pattern: The regular expression pattern to match.
        :param options: A bitwise combination of the enumeration values that specify options for matching.
        :param matchTimeout: A time-out interval, or InfiniteMatchTimeout to indicate that the method should not time out.
        :returns: A ValueMatchEnumerator to iterate over the matches.
        """
        ...

    @overload
    def EnumerateMatches(self, input: System.ReadOnlySpan[str]) -> System.Text.RegularExpressions.Regex.ValueMatchEnumerator:
        """
        Searches an input span for all occurrences of a regular expression and returns a ValueMatchEnumerator to iterate over the matches.
        
        :param input: The span to search for a match.
        :returns: A ValueMatchEnumerator to iterate over the matches.
        """
        ...

    @overload
    def EnumerateMatches(self, input: System.ReadOnlySpan[str], startat: int) -> System.Text.RegularExpressions.Regex.ValueMatchEnumerator:
        """
        Searches an input span for all occurrences of a regular expression and returns a ValueMatchEnumerator to iterate over the matches.
        
        :param input: The span to search for a match.
        :param startat: The zero-based character position at which to start the search.
        :returns: A ValueMatchEnumerator to iterate over the matches.
        """
        ...

    @staticmethod
    def Escape(str: str) -> str:
        """
        Escapes a minimal set of metacharacters (\\, *, +, ?, |, {, [, (, ), ^, $, ., #, and
        whitespace) by replacing them with their \\ codes. This converts a string so that
        it can be used as a constant within a regular expression safely. (Note that the
        reason # and whitespace must be escaped is so the string can be used safely
        within an expression parsed with x mode. If future Regex features add
        additional metacharacters, developers should depend on Escape to escape those
        characters as well.)
        """
        ...

    def GetGroupNames(self) -> typing.List[str]:
        """
        Returns the GroupNameCollection for the regular expression. This collection contains the
        set of strings used to name capturing groups in the expression.
        """
        ...

    def GetGroupNumbers(self) -> typing.List[int]:
        """Returns the integer group number corresponding to a group name."""
        ...

    def GroupNameFromNumber(self, i: int) -> str:
        """Retrieves a group name that corresponds to a group number."""
        ...

    def GroupNumberFromName(self, name: str) -> int:
        """Returns a group number that corresponds to a group name, or -1 if the name is not a recognized group name."""
        ...

    def InitializeReferences(self) -> None:
        """
        This method is protected.
        
        Obsoletions.RegexExtensibilityImplMessage
        """
        warnings.warn("Obsoletions.RegexExtensibilityImplMessage", DeprecationWarning)

    @staticmethod
    @overload
    def IsMatch(input: str, pattern: str) -> bool:
        """Searches the input string for one or more occurrences of the text supplied in the given pattern."""
        ...

    @staticmethod
    @overload
    def IsMatch(input: System.ReadOnlySpan[str], pattern: str) -> bool:
        """
        Indicates whether the specified regular expression finds a match in the specified input span.
        
        :param input: The span to search for a match.
        :param pattern: The regular expression pattern to match.
        :returns: true if the regular expression finds a match; otherwise, false.
        """
        ...

    @staticmethod
    @overload
    def IsMatch(input: str, pattern: str, options: System.Text.RegularExpressions.RegexOptions) -> bool:
        """
        Searches the input string for one or more occurrences of the text
        supplied in the pattern parameter with matching options supplied in the options
        parameter.
        """
        ...

    @staticmethod
    @overload
    def IsMatch(input: System.ReadOnlySpan[str], pattern: str, options: System.Text.RegularExpressions.RegexOptions) -> bool:
        """
        Indicates whether the specified regular expression finds a match in the specified input span, using the specified matching options.
        
        :param input: The span to search for a match.
        :param pattern: The regular expression pattern to match.
        :param options: A bitwise combination of the enumeration values that provide options for matching.
        :returns: true if the regular expression finds a match; otherwise, false.
        """
        ...

    @staticmethod
    @overload
    def IsMatch(input: str, pattern: str, options: System.Text.RegularExpressions.RegexOptions, matchTimeout: datetime.timedelta) -> bool:
        ...

    @staticmethod
    @overload
    def IsMatch(input: System.ReadOnlySpan[str], pattern: str, options: System.Text.RegularExpressions.RegexOptions, matchTimeout: datetime.timedelta) -> bool:
        """
        Indicates whether the specified regular expression finds a match in the specified input span, using the specified matching options and time-out interval.
        
        :param input: The span to search for a match.
        :param pattern: The regular expression pattern to match.
        :param options: A bitwise combination of the enumeration values that provide options for matching.
        :param matchTimeout: A time-out interval, or Regex.InfiniteMatchTimeout to indicate that the method should not time out.
        :returns: true if the regular expression finds a match; otherwise, false.
        """
        ...

    @overload
    def IsMatch(self, input: str) -> bool:
        """
        Searches the input string for one or more matches using the previous pattern,
        options, and starting position.
        """
        ...

    @overload
    def IsMatch(self, input: str, startat: int) -> bool:
        """
        Searches the input string for one or more matches using the previous pattern and options,
        with a new starting position.
        """
        ...

    @overload
    def IsMatch(self, input: System.ReadOnlySpan[str]) -> bool:
        """
        Indicates whether the regular expression specified in the Regex constructor finds a match in a specified input span.
        
        :param input: The span to search for a match.
        :returns: true if the regular expression finds a match; otherwise, false.
        """
        ...

    @overload
    def IsMatch(self, input: System.ReadOnlySpan[str], startat: int) -> bool:
        """
        Indicates whether the regular expression specified in the Regex constructor finds a match in a specified input span.
        
        :param input: The span to search for a match.
        :param startat: The zero-based character position at which to start the search.
        :returns: true if the regular expression finds a match; otherwise, false.
        """
        ...

    @staticmethod
    @overload
    def Match(input: str, pattern: str) -> System.Text.RegularExpressions.Match:
        """
        Searches the input string for one or more occurrences of the text
        supplied in the pattern parameter.
        """
        ...

    @staticmethod
    @overload
    def Match(input: str, pattern: str, options: System.Text.RegularExpressions.RegexOptions) -> System.Text.RegularExpressions.Match:
        """
        Searches the input string for one or more occurrences of the text
        supplied in the pattern parameter. Matching is modified with an option
        string.
        """
        ...

    @staticmethod
    @overload
    def Match(input: str, pattern: str, options: System.Text.RegularExpressions.RegexOptions, matchTimeout: datetime.timedelta) -> System.Text.RegularExpressions.Match:
        ...

    @overload
    def Match(self, input: str) -> System.Text.RegularExpressions.Match:
        """
        Matches a regular expression with a string and returns
        the precise result as a Match object.
        """
        ...

    @overload
    def Match(self, input: str, startat: int) -> System.Text.RegularExpressions.Match:
        """
        Matches a regular expression with a string and returns
        the precise result as a Match object.
        """
        ...

    @overload
    def Match(self, input: str, beginning: int, length: int) -> System.Text.RegularExpressions.Match:
        """Matches a regular expression with a string and returns the precise result as a Match object."""
        ...

    @staticmethod
    @overload
    def Matches(input: str, pattern: str) -> System.Text.RegularExpressions.MatchCollection:
        """Returns all the successful matches as if Match were called iteratively numerous times."""
        ...

    @staticmethod
    @overload
    def Matches(input: str, pattern: str, options: System.Text.RegularExpressions.RegexOptions) -> System.Text.RegularExpressions.MatchCollection:
        """Returns all the successful matches as if Match were called iteratively numerous times."""
        ...

    @staticmethod
    @overload
    def Matches(input: str, pattern: str, options: System.Text.RegularExpressions.RegexOptions, matchTimeout: datetime.timedelta) -> System.Text.RegularExpressions.MatchCollection:
        ...

    @overload
    def Matches(self, input: str) -> System.Text.RegularExpressions.MatchCollection:
        """Returns all the successful matches as if Match was called iteratively numerous times."""
        ...

    @overload
    def Matches(self, input: str, startat: int) -> System.Text.RegularExpressions.MatchCollection:
        """Returns all the successful matches as if Match was called iteratively numerous times."""
        ...

    @staticmethod
    @overload
    def Replace(input: str, pattern: str, replacement: str) -> str:
        """
        Replaces all occurrences of the pattern with the  pattern, starting at
        the first character in the input string.
        """
        ...

    @staticmethod
    @overload
    def Replace(input: str, pattern: str, replacement: str, options: System.Text.RegularExpressions.RegexOptions) -> str:
        """
        Replaces all occurrences of
        the with the 
        pattern, starting at the first character in the input string.
        """
        ...

    @staticmethod
    @overload
    def Replace(input: str, pattern: str, replacement: str, options: System.Text.RegularExpressions.RegexOptions, matchTimeout: datetime.timedelta) -> str:
        ...

    @overload
    def Replace(self, input: str, replacement: str) -> str:
        """
        Replaces all occurrences of the previously defined pattern with the
         pattern, starting at the first character in the
        input string.
        """
        ...

    @overload
    def Replace(self, input: str, replacement: str, count: int) -> str:
        """
        Replaces all occurrences of the previously defined pattern with the
         pattern, starting at the first character in the
        input string.
        """
        ...

    @overload
    def Replace(self, input: str, replacement: str, count: int, startat: int) -> str:
        """
        Replaces all occurrences of the previously defined pattern with the
         pattern, starting at the character position
        .
        """
        ...

    @staticmethod
    @overload
    def Replace(input: str, pattern: str, evaluator: typing.Callable[[System.Text.RegularExpressions.Match], str]) -> str:
        """
        Replaces all occurrences of the  with the recent
        replacement pattern.
        """
        ...

    @staticmethod
    @overload
    def Replace(input: str, pattern: str, evaluator: typing.Callable[[System.Text.RegularExpressions.Match], str], options: System.Text.RegularExpressions.RegexOptions) -> str:
        """
        Replaces all occurrences of the  with the recent
        replacement pattern, starting at the first character.
        """
        ...

    @staticmethod
    @overload
    def Replace(input: str, pattern: str, evaluator: typing.Callable[[System.Text.RegularExpressions.Match], str], options: System.Text.RegularExpressions.RegexOptions, matchTimeout: datetime.timedelta) -> str:
        ...

    @overload
    def Replace(self, input: str, evaluator: typing.Callable[[System.Text.RegularExpressions.Match], str]) -> str:
        """
        Replaces all occurrences of the previously defined pattern with the recent
        replacement pattern, starting at the first character position.
        """
        ...

    @overload
    def Replace(self, input: str, evaluator: typing.Callable[[System.Text.RegularExpressions.Match], str], count: int) -> str:
        """
        Replaces all occurrences of the previously defined pattern with the recent
        replacement pattern, starting at the first character position.
        """
        ...

    @overload
    def Replace(self, input: str, evaluator: typing.Callable[[System.Text.RegularExpressions.Match], str], count: int, startat: int) -> str:
        """
        Replaces all occurrences of the previously defined pattern with the recent
        replacement pattern, starting at the character position
        .
        """
        ...

    @staticmethod
    @overload
    def Split(input: str, pattern: str) -> typing.List[str]:
        """
        Splits the string at the position defined
        by .
        """
        ...

    @staticmethod
    @overload
    def Split(input: str, pattern: str, options: System.Text.RegularExpressions.RegexOptions) -> typing.List[str]:
        """Splits the string at the position defined by ."""
        ...

    @staticmethod
    @overload
    def Split(input: str, pattern: str, options: System.Text.RegularExpressions.RegexOptions, matchTimeout: datetime.timedelta) -> typing.List[str]:
        ...

    @overload
    def Split(self, input: str) -> typing.List[str]:
        """
        Splits the  string at the position defined by a
        previous pattern.
        """
        ...

    @overload
    def Split(self, input: str, count: int) -> typing.List[str]:
        """
        Splits the  string at the position defined by a
        previous pattern.
        """
        ...

    @overload
    def Split(self, input: str, count: int, startat: int) -> typing.List[str]:
        """Splits the  string at the position defined by a previous pattern."""
        ...

    def ToString(self) -> str:
        """Returns the regular expression pattern passed into the constructor"""
        ...

    @staticmethod
    def Unescape(str: str) -> str:
        """Unescapes any escaped characters in the input string."""
        ...

    def UseOptionC(self) -> bool:
        """
        True if the RegexOptions.Compiled option was set.
        
        This method is protected.
        
        Obsoletions.RegexExtensibilityImplMessage
        """
        warnings.warn("Obsoletions.RegexExtensibilityImplMessage", DeprecationWarning)

    def UseOptionR(self) -> bool:
        """
        True if the RegexOptions.RightToLeft option was set.
        
        This method is protected.
        
        Obsoletions.RegexExtensibilityImplMessage
        """
        warnings.warn("Obsoletions.RegexExtensibilityImplMessage", DeprecationWarning)


class GeneratedRegexAttribute(System.Attribute):
    """Instructs the System.Text.RegularExpressions source generator to generate an implementation of the specified regular expression."""

    @property
    def Pattern(self) -> str:
        """Gets the regular expression pattern to match."""
        ...

    @property
    def Options(self) -> System.Text.RegularExpressions.RegexOptions:
        """Gets a bitwise combination of the enumeration values that modify the regular expression."""
        ...

    @property
    def MatchTimeoutMilliseconds(self) -> int:
        """Gets a time-out interval (milliseconds), or Timeout.Infinite to indicate that the method should not time out."""
        ...

    @property
    def CultureName(self) -> str:
        """Gets the name of the culture to be used for case sensitive comparisons."""
        ...

    @overload
    def __init__(self, pattern: str) -> None:
        """
        Initializes a new instance of the GeneratedRegexAttribute with the specified pattern.
        
        :param pattern: The regular expression pattern to match.
        """
        ...

    @overload
    def __init__(self, pattern: str, options: System.Text.RegularExpressions.RegexOptions) -> None:
        """
        Initializes a new instance of the GeneratedRegexAttribute with the specified pattern and options.
        
        :param pattern: The regular expression pattern to match.
        :param options: A bitwise combination of the enumeration values that modify the regular expression.
        """
        ...

    @overload
    def __init__(self, pattern: str, options: System.Text.RegularExpressions.RegexOptions, cultureName: str) -> None:
        """
        Initializes a new instance of the GeneratedRegexAttribute with the specified pattern and options.
        
        :param pattern: The regular expression pattern to match.
        :param options: A bitwise combination of the enumeration values that modify the regular expression.
        :param cultureName: The name of a culture to be used for case sensitive comparisons.  is not case-sensitive.
        """
        ...

    @overload
    def __init__(self, pattern: str, options: System.Text.RegularExpressions.RegexOptions, matchTimeoutMilliseconds: int) -> None:
        """
        Initializes a new instance of the GeneratedRegexAttribute with the specified pattern, options, and timeout.
        
        :param pattern: The regular expression pattern to match.
        :param options: A bitwise combination of the enumeration values that modify the regular expression.
        :param matchTimeoutMilliseconds: A time-out interval (milliseconds), or Timeout.Infinite to indicate that the method should not time out.
        """
        ...

    @overload
    def __init__(self, pattern: str, options: System.Text.RegularExpressions.RegexOptions, matchTimeoutMilliseconds: int, cultureName: str) -> None:
        """
        Initializes a new instance of the GeneratedRegexAttribute with the specified pattern, options, and timeout.
        
        :param pattern: The regular expression pattern to match.
        :param options: A bitwise combination of the enumeration values that modify the regular expression.
        :param matchTimeoutMilliseconds: A time-out interval (milliseconds), or Timeout.Infinite to indicate that the method should not time out.
        :param cultureName: The name of a culture to be used for case sensitive comparisons.  is not case-sensitive.
        """
        ...


class RegexMatchTimeoutException(System.TimeoutException, System.Runtime.Serialization.ISerializable):
    """This is the exception that is thrown when a RegEx matching timeout occurs."""

    @property
    def Input(self) -> str:
        ...

    @property
    def Pattern(self) -> str:
        ...

    @property
    def MatchTimeout(self) -> datetime.timedelta:
        ...

    @overload
    def __init__(self, regexInput: str, regexPattern: str, matchTimeout: datetime.timedelta) -> None:
        """
        Constructs a new RegexMatchTimeoutException.
        
        :param regexInput: Matching timeout occurred during matching within the specified input.
        :param regexPattern: Matching timeout occurred during matching to the specified pattern.
        :param matchTimeout: Matching timeout occurred because matching took longer than the specified timeout.
        """
        ...

    @overload
    def __init__(self) -> None:
        """
        This constructor is provided in compliance with common .NET Framework design patterns;
        developers should prefer using the constructor
        public RegexMatchTimeoutException(string input, string pattern, TimeSpan matchTimeout).
        """
        ...

    @overload
    def __init__(self, message: str) -> None:
        """
        This constructor is provided in compliance with common .NET Framework design patterns;
        developers should prefer using the constructor
        public RegexMatchTimeoutException(string input, string pattern, TimeSpan matchTimeout).
        
        :param message: The error message that explains the reason for the exception.
        """
        ...

    @overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        """
        This constructor is provided in compliance with common .NET Framework design patterns;
        developers should prefer using the constructor
        public RegexMatchTimeoutException(string input, string pattern, TimeSpan matchTimeout).
        
        :param message: The error message that explains the reason for the exception.
        :param inner: The exception that is the cause of the current exception, or a null.
        """
        ...

    @overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        This method is protected.
        
        Obsoletions.LegacyFormatterImplMessage
        """
        ...


class RegexRunnerFactory(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __init__(self) -> None:
        """This method is protected."""
        ...


class RegexRunner(System.Object, metaclass=abc.ABCMeta):
    """
    Base class for source-generated regex extensibility
    (and the old CompileToAssembly extensibility).
    It's not intended to be used by anything else.
    """

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def Capture(self, capnum: int, start: int, end: int) -> None:
        """
        Called by Go() to capture a subexpression. Note that the
        capnum used here has already been mapped to a non-sparse
        index (by the code generator RegexWriter).
        
        This method is protected.
        """
        ...

    @staticmethod
    def CharInClass(ch: str, charClass: str) -> bool:
        ...

    @staticmethod
    def CharInSet(ch: str, set: str, category: str) -> bool:
        """
        This method is protected.
        
        Obsoletions.RegexExtensibilityImplMessage
        """
        warnings.warn("Obsoletions.RegexExtensibilityImplMessage", DeprecationWarning)

    def Crawl(self, i: int) -> None:
        """
        Save a number on the longjump unrolling stack
        
        This method is protected.
        """
        ...

    def Crawlpos(self) -> int:
        """
        Get the height of the stack
        
        This method is protected.
        """
        ...

    def DoubleCrawl(self) -> None:
        """
        Increases the size of the longjump unrolling stack.
        
        This method is protected.
        """
        ...

    def DoubleStack(self) -> None:
        """
        Called by the implementation of Go() to increase the size of the
        grouping stack.
        
        This method is protected.
        """
        ...

    def DoubleTrack(self) -> None:
        """
        Called by the implementation of Go() to increase the size of the
        backtracking stack.
        
        This method is protected.
        """
        ...

    def EnsureStorage(self) -> None:
        """
        Called by the implementation of Go() to increase the size of storage
        
        This method is protected.
        """
        ...

    def FindFirstChar(self) -> bool:
        """
        The responsibility of FindFirstChar() is to advance runtextpos
        until it is at the next position which is a candidate for the
        beginning of a successful match.
        
        This method is protected.
        """
        ...

    def Go(self) -> None:
        """
        The responsibility of Go() is to run the regular expression at
        runtextpos and call Capture() on all the captured subexpressions,
        then to leave runtextpos at the ending position. It should leave
        runtextpos where it started if there was no match.
        
        This method is protected.
        """
        ...

    def InitTrackCount(self) -> None:
        """
        InitTrackCount must initialize the runtrackcount field; this is
        used to know how large the initial runtrack and runstack arrays
        must be.
        
        This method is protected.
        """
        ...

    def IsBoundary(self, index: int, startpos: int, endpos: int) -> bool:
        """
        Called by the implementation of Go() to decide whether the pos
        at the specified index is a boundary or not. It's just not worth
        emitting inline code for this logic.
        
        This method is protected.
        """
        ...

    def IsECMABoundary(self, index: int, startpos: int, endpos: int) -> bool:
        """This method is protected."""
        ...

    def IsMatched(self, cap: int) -> bool:
        """
        Call out to runmatch to get around visibility issues
        
        This method is protected.
        """
        ...

    def MatchIndex(self, cap: int) -> int:
        """
        Call out to runmatch to get around visibility issues
        
        This method is protected.
        """
        ...

    def MatchLength(self, cap: int) -> int:
        """
        Call out to runmatch to get around visibility issues
        
        This method is protected.
        """
        ...

    def Popcrawl(self) -> int:
        """
        Remove a number from the longjump unrolling stack
        
        This method is protected.
        """
        ...

    def Scan(self, regex: System.Text.RegularExpressions.Regex, text: str, textbeg: int, textend: int, textstart: int, prevlen: int, quick: bool) -> System.Text.RegularExpressions.Match:
        """
        This method is protected.
        
        Obsoletions.RegexExtensibilityImplMessage
        """
        warnings.warn("Obsoletions.RegexExtensibilityImplMessage", DeprecationWarning)

    def TransferCapture(self, capnum: int, uncapnum: int, start: int, end: int) -> None:
        """
        Called by Go() to capture a subexpression. Note that the
        capnum used here has already been mapped to a non-sparse
        index (by the code generator RegexWriter).
        
        This method is protected.
        """
        ...

    def Uncapture(self) -> None:
        """This method is protected."""
        ...


