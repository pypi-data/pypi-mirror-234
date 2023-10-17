from typing import overload
import typing

import System
import System.Buffers.Binary


class BinaryPrimitives(System.Object):
    """This class has no documentation."""

    @staticmethod
    def ReadDoubleBigEndian(source: System.ReadOnlySpan[int]) -> float:
        """
        Reads a double from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadDoubleLittleEndian(source: System.ReadOnlySpan[int]) -> float:
        """
        Reads a double from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadHalfBigEndian(source: System.ReadOnlySpan[int]) -> System.Half:
        """
        Reads a Half from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadHalfLittleEndian(source: System.ReadOnlySpan[int]) -> System.Half:
        """
        Reads a Half from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadInt128BigEndian(source: System.ReadOnlySpan[int]) -> System.Int128:
        """
        Reads a Int128 from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadInt128LittleEndian(source: System.ReadOnlySpan[int]) -> System.Int128:
        """
        Reads a Int128 from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadInt16BigEndian(source: System.ReadOnlySpan[int]) -> int:
        """
        Reads a short from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadInt16LittleEndian(source: System.ReadOnlySpan[int]) -> int:
        """
        Reads a short from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadInt32BigEndian(source: System.ReadOnlySpan[int]) -> int:
        """
        Reads a int from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadInt32LittleEndian(source: System.ReadOnlySpan[int]) -> int:
        """
        Reads a int from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadInt64BigEndian(source: System.ReadOnlySpan[int]) -> int:
        """
        Reads a long from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadInt64LittleEndian(source: System.ReadOnlySpan[int]) -> int:
        """
        Reads a long from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadIntPtrBigEndian(source: System.ReadOnlySpan[int]) -> System.IntPtr:
        """
        Reads a nint from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadIntPtrLittleEndian(source: System.ReadOnlySpan[int]) -> System.IntPtr:
        """
        Reads a nint from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadSingleBigEndian(source: System.ReadOnlySpan[int]) -> float:
        """
        Reads a float from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadSingleLittleEndian(source: System.ReadOnlySpan[int]) -> float:
        """
        Reads a float from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadUInt128BigEndian(source: System.ReadOnlySpan[int]) -> System.UInt128:
        """
        Reads a UInt128 from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadUInt128LittleEndian(source: System.ReadOnlySpan[int]) -> System.UInt128:
        """
        Reads a UInt128 from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadUInt16BigEndian(source: System.ReadOnlySpan[int]) -> int:
        """
        Reads a ushort from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadUInt16LittleEndian(source: System.ReadOnlySpan[int]) -> int:
        """
        Reads a ushort from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadUInt32BigEndian(source: System.ReadOnlySpan[int]) -> int:
        """
        Reads a uint from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadUInt32LittleEndian(source: System.ReadOnlySpan[int]) -> int:
        """
        Reads a uint from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadUInt64BigEndian(source: System.ReadOnlySpan[int]) -> int:
        """
        Reads a ulong from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadUInt64LittleEndian(source: System.ReadOnlySpan[int]) -> int:
        """
        Reads a ulong from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    def ReadUIntPtrBigEndian(source: System.ReadOnlySpan[int]) -> System.UIntPtr:
        """
        Reads a nuint from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span to read.
        :returns: The big endian value.
        """
        ...

    @staticmethod
    def ReadUIntPtrLittleEndian(source: System.ReadOnlySpan[int]) -> System.UIntPtr:
        """
        Reads a nuint from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span to read.
        :returns: The little endian value.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(value: int) -> int:
        """
        Reverses a primitive value by performing an endianness swap of the specified sbyte value, which effectively does nothing for an sbyte.
        
        :param value: The value to reverse.
        :returns: The passed-in value, unmodified.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(value: int) -> int:
        """
        Reverses a primitive value by performing an endianness swap of the specified short value.
        
        :param value: The value to reverse.
        :returns: The reversed value.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(value: int) -> int:
        """
        Reverses a primitive value by performing an endianness swap of the specified int value.
        
        :param value: The value to reverse.
        :returns: The reversed value.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(value: int) -> int:
        """
        Reverses a primitive value by performing an endianness swap of the specified long value.
        
        :param value: The value to reverse.
        :returns: The reversed value.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(value: System.IntPtr) -> System.IntPtr:
        """
        Reverses a primitive value by performing an endianness swap of the specified nint value.
        
        :param value: The value to reverse.
        :returns: The reversed value.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(value: System.Int128) -> System.Int128:
        """
        Reverses a primitive value by performing an endianness swap of the specified Int128 value.
        
        :param value: The value to reverse.
        :returns: The reversed value.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(value: int) -> int:
        """
        Reverses a primitive value by performing an endianness swap of the specified byte value, which effectively does nothing for an byte.
        
        :param value: The value to reverse.
        :returns: The passed-in value, unmodified.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(value: int) -> int:
        """
        Reverses a primitive value by performing an endianness swap of the specified ushort value.
        
        :param value: The value to reverse.
        :returns: The reversed value.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(value: int) -> int:
        """
        Reverses a primitive value by performing an endianness swap of the specified uint value.
        
        :param value: The value to reverse.
        :returns: The reversed value.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(value: int) -> int:
        """
        Reverses a primitive value by performing an endianness swap of the specified ulong value.
        
        :param value: The value to reverse.
        :returns: The reversed value.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(value: System.UIntPtr) -> System.UIntPtr:
        """
        Reverses a primitive value by performing an endianness swap of the specified nuint value.
        
        :param value: The value to reverse.
        :returns: The reversed value.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(value: System.UInt128) -> System.UInt128:
        """
        Reverses a primitive value by performing an endianness swap of the specified UInt128 value.
        
        :param value: The value to reverse.
        :returns: The reversed value.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(source: System.ReadOnlySpan[int], destination: System.Span[int]) -> None:
        """
        Copies every primitive value from  to , reversing each primitive by performing an endianness swap as part of writing each.
        
        :param source: The source span to copy.
        :param destination: The destination to which the source elements should be copied.
        """
        ...

    @staticmethod
    @overload
    def ReverseEndianness(source: System.ReadOnlySpan[int], destination: System.Span[int]) -> None:
        ...

    @staticmethod
    @overload
    def ReverseEndianness(source: System.ReadOnlySpan[int], destination: System.Span[int]) -> None:
        ...

    @staticmethod
    @overload
    def ReverseEndianness(source: System.ReadOnlySpan[int], destination: System.Span[int]) -> None:
        ...

    @staticmethod
    @overload
    def ReverseEndianness(source: System.ReadOnlySpan[int], destination: System.Span[int]) -> None:
        ...

    @staticmethod
    @overload
    def ReverseEndianness(source: System.ReadOnlySpan[int], destination: System.Span[int]) -> None:
        ...

    @staticmethod
    @overload
    def ReverseEndianness(source: System.ReadOnlySpan[System.UIntPtr], destination: System.Span[System.UIntPtr]) -> None:
        ...

    @staticmethod
    @overload
    def ReverseEndianness(source: System.ReadOnlySpan[System.IntPtr], destination: System.Span[System.IntPtr]) -> None:
        ...

    @staticmethod
    @overload
    def ReverseEndianness(source: System.ReadOnlySpan[System.UInt128], destination: System.Span[System.UInt128]) -> None:
        ...

    @staticmethod
    @overload
    def ReverseEndianness(source: System.ReadOnlySpan[System.Int128], destination: System.Span[System.Int128]) -> None:
        ...

    @staticmethod
    def TryReadDoubleBigEndian(source: System.ReadOnlySpan[int], value: typing.Optional[float]) -> typing.Union[bool, float]:
        """
        Reads a double from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a double; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadDoubleLittleEndian(source: System.ReadOnlySpan[int], value: typing.Optional[float]) -> typing.Union[bool, float]:
        """
        Reads a double from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a double; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadHalfBigEndian(source: System.ReadOnlySpan[int], value: typing.Optional[System.Half]) -> typing.Union[bool, System.Half]:
        """
        Reads a Half from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a Half; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadHalfLittleEndian(source: System.ReadOnlySpan[int], value: typing.Optional[System.Half]) -> typing.Union[bool, System.Half]:
        """
        Reads a Half from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a Half; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadInt128BigEndian(source: System.ReadOnlySpan[int], value: typing.Optional[System.Int128]) -> typing.Union[bool, System.Int128]:
        """
        Reads a Int128 from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a Int128; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadInt128LittleEndian(source: System.ReadOnlySpan[int], value: typing.Optional[System.Int128]) -> typing.Union[bool, System.Int128]:
        """
        Reads a Int128 from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a Int128; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadInt16BigEndian(source: System.ReadOnlySpan[int], value: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Reads a short from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a short; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadInt16LittleEndian(source: System.ReadOnlySpan[int], value: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Reads a short from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a short; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadInt32BigEndian(source: System.ReadOnlySpan[int], value: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Reads a int from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a int; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadInt32LittleEndian(source: System.ReadOnlySpan[int], value: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Reads a int from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a int; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadInt64BigEndian(source: System.ReadOnlySpan[int], value: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Reads a long from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a long; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadInt64LittleEndian(source: System.ReadOnlySpan[int], value: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Reads a long from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a long; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadIntPtrBigEndian(source: System.ReadOnlySpan[int], value: typing.Optional[System.IntPtr]) -> typing.Union[bool, System.IntPtr]:
        """
        Reads a nint from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a nint; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadIntPtrLittleEndian(source: System.ReadOnlySpan[int], value: typing.Optional[System.IntPtr]) -> typing.Union[bool, System.IntPtr]:
        """
        Reads a nint from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a nint; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadSingleBigEndian(source: System.ReadOnlySpan[int], value: typing.Optional[float]) -> typing.Union[bool, float]:
        """
        Reads a float from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a float; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadSingleLittleEndian(source: System.ReadOnlySpan[int], value: typing.Optional[float]) -> typing.Union[bool, float]:
        """
        Reads a float from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a float; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadUInt128BigEndian(source: System.ReadOnlySpan[int], value: typing.Optional[System.UInt128]) -> typing.Union[bool, System.UInt128]:
        """
        Reads a UInt128 from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a UInt128; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadUInt128LittleEndian(source: System.ReadOnlySpan[int], value: typing.Optional[System.UInt128]) -> typing.Union[bool, System.UInt128]:
        """
        Reads a UInt128 from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a UInt128; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadUInt16BigEndian(source: System.ReadOnlySpan[int], value: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Reads a ushort from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a ushort; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadUInt16LittleEndian(source: System.ReadOnlySpan[int], value: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Reads a ushort from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a ushort; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadUInt32BigEndian(source: System.ReadOnlySpan[int], value: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Reads a uint from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a uint; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadUInt32LittleEndian(source: System.ReadOnlySpan[int], value: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Reads a uint from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a uint; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadUInt64BigEndian(source: System.ReadOnlySpan[int], value: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Reads a ulong from the beginning of a read-only span of bytes, as big endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as big endian.
        :returns: true if the span is large enough to contain a ulong; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadUInt64LittleEndian(source: System.ReadOnlySpan[int], value: typing.Optional[int]) -> typing.Union[bool, int]:
        """
        Reads a ulong from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a ulong; otherwise, false.
        """
        ...

    @staticmethod
    def TryReadUIntPtrBigEndian(source: System.ReadOnlySpan[int], value: typing.Optional[System.UIntPtr]) -> typing.Union[bool, System.UIntPtr]:
        ...

    @staticmethod
    def TryReadUIntPtrLittleEndian(source: System.ReadOnlySpan[int], value: typing.Optional[System.UIntPtr]) -> typing.Union[bool, System.UIntPtr]:
        """
        Reads a nuint from the beginning of a read-only span of bytes, as little endian.
        
        :param source: The read-only span of bytes to read.
        :param value: When this method returns, contains the value read out of the read-only span of bytes, as little endian.
        :returns: true if the span is large enough to contain a nuint; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteDoubleBigEndian(destination: System.Span[int], value: float) -> bool:
        """
        Writes a double into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a double; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteDoubleLittleEndian(destination: System.Span[int], value: float) -> bool:
        """
        Writes a double into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a double; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteHalfBigEndian(destination: System.Span[int], value: System.Half) -> bool:
        """
        Writes a Half into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a Half; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteHalfLittleEndian(destination: System.Span[int], value: System.Half) -> bool:
        """
        Writes a Half into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a Half; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteInt128BigEndian(destination: System.Span[int], value: System.Int128) -> bool:
        """
        Writes a Int128 into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a Int128; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteInt128LittleEndian(destination: System.Span[int], value: System.Int128) -> bool:
        """
        Writes a Int128 into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a Int128; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteInt16BigEndian(destination: System.Span[int], value: int) -> bool:
        """
        Writes a short into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a short; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteInt16LittleEndian(destination: System.Span[int], value: int) -> bool:
        """
        Writes a short into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a short; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteInt32BigEndian(destination: System.Span[int], value: int) -> bool:
        """
        Writes a int into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a int; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteInt32LittleEndian(destination: System.Span[int], value: int) -> bool:
        """
        Writes a int into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a int; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteInt64BigEndian(destination: System.Span[int], value: int) -> bool:
        """
        Writes a long into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a long; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteInt64LittleEndian(destination: System.Span[int], value: int) -> bool:
        """
        Writes a long into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a long; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteIntPtrBigEndian(destination: System.Span[int], value: System.IntPtr) -> bool:
        """
        Writes a nint into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a nint; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteIntPtrLittleEndian(destination: System.Span[int], value: System.IntPtr) -> bool:
        """
        Writes a nint into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a nint; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteSingleBigEndian(destination: System.Span[int], value: float) -> bool:
        """
        Writes a float into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a float; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteSingleLittleEndian(destination: System.Span[int], value: float) -> bool:
        """
        Writes a float into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a float; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteUInt128BigEndian(destination: System.Span[int], value: System.UInt128) -> bool:
        """
        Writes a UInt128 into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a UInt128; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteUInt128LittleEndian(destination: System.Span[int], value: System.UInt128) -> bool:
        """
        Writes a UInt128 into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a UInt128; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteUInt16BigEndian(destination: System.Span[int], value: int) -> bool:
        """
        Write a ushort into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a ushort; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteUInt16LittleEndian(destination: System.Span[int], value: int) -> bool:
        """
        Write a ushort into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a ushort; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteUInt32BigEndian(destination: System.Span[int], value: int) -> bool:
        """
        Write a uint into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a uint; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteUInt32LittleEndian(destination: System.Span[int], value: int) -> bool:
        """
        Write a uint into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a uint; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteUInt64BigEndian(destination: System.Span[int], value: int) -> bool:
        """
        Write a ulong into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a ulong; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteUInt64LittleEndian(destination: System.Span[int], value: int) -> bool:
        """
        Write a ulong into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a ulong; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteUIntPtrBigEndian(destination: System.Span[int], value: System.UIntPtr) -> bool:
        """
        Writes a nuint into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a nuint; otherwise, false.
        """
        ...

    @staticmethod
    def TryWriteUIntPtrLittleEndian(destination: System.Span[int], value: System.UIntPtr) -> bool:
        """
        Writes a nuint into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        :returns: true if the span is large enough to contain a nuint; otherwise, false.
        """
        ...

    @staticmethod
    def WriteDoubleBigEndian(destination: System.Span[int], value: float) -> None:
        """
        Writes a double into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteDoubleLittleEndian(destination: System.Span[int], value: float) -> None:
        """
        Writes a double into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteHalfBigEndian(destination: System.Span[int], value: System.Half) -> None:
        """
        Writes a Half into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteHalfLittleEndian(destination: System.Span[int], value: System.Half) -> None:
        """
        Writes a Half into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteInt128BigEndian(destination: System.Span[int], value: System.Int128) -> None:
        """
        Writes a Int128 into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteInt128LittleEndian(destination: System.Span[int], value: System.Int128) -> None:
        """
        Writes a Int128 into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteInt16BigEndian(destination: System.Span[int], value: int) -> None:
        """
        Writes a short into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteInt16LittleEndian(destination: System.Span[int], value: int) -> None:
        """
        Writes a short into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteInt32BigEndian(destination: System.Span[int], value: int) -> None:
        """
        Writes a int into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteInt32LittleEndian(destination: System.Span[int], value: int) -> None:
        """
        Writes a int into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteInt64BigEndian(destination: System.Span[int], value: int) -> None:
        """
        Writes a long into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteInt64LittleEndian(destination: System.Span[int], value: int) -> None:
        """
        Writes a long into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteIntPtrBigEndian(destination: System.Span[int], value: System.IntPtr) -> None:
        """
        Writes a nint into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteIntPtrLittleEndian(destination: System.Span[int], value: System.IntPtr) -> None:
        """
        Writes a nint into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteSingleBigEndian(destination: System.Span[int], value: float) -> None:
        """
        Writes a float into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteSingleLittleEndian(destination: System.Span[int], value: float) -> None:
        """
        Writes a float into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteUInt128BigEndian(destination: System.Span[int], value: System.UInt128) -> None:
        """
        Writes a UInt128 into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteUInt128LittleEndian(destination: System.Span[int], value: System.UInt128) -> None:
        """
        Writes a UInt128 into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteUInt16BigEndian(destination: System.Span[int], value: int) -> None:
        """
        Write a ushort into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteUInt16LittleEndian(destination: System.Span[int], value: int) -> None:
        """
        Write a ushort into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteUInt32BigEndian(destination: System.Span[int], value: int) -> None:
        """
        Write a uint into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteUInt32LittleEndian(destination: System.Span[int], value: int) -> None:
        """
        Write a uint into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteUInt64BigEndian(destination: System.Span[int], value: int) -> None:
        """
        Write a ulong into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteUInt64LittleEndian(destination: System.Span[int], value: int) -> None:
        """
        Write a ulong into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteUIntPtrBigEndian(destination: System.Span[int], value: System.UIntPtr) -> None:
        """
        Writes a nuint into a span of bytes, as big endian.
        
        :param destination: The span of bytes where the value is to be written, as big endian.
        :param value: The value to write into the span of bytes.
        """
        ...

    @staticmethod
    def WriteUIntPtrLittleEndian(destination: System.Span[int], value: System.UIntPtr) -> None:
        """
        Writes a nuint into a span of bytes, as little endian.
        
        :param destination: The span of bytes where the value is to be written, as little endian.
        :param value: The value to write into the span of bytes.
        """
        ...


