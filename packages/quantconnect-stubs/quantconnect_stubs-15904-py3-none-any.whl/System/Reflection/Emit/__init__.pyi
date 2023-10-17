from typing import overload
import abc
import typing
import warnings

import System
import System.Collections.Generic
import System.Globalization
import System.IO
import System.Reflection
import System.Reflection.Emit
import System.Runtime.InteropServices

System_Reflection_Emit_Label = typing.Any
System_Reflection_Emit_OpCode = typing.Any


class ParameterBuilder(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def Attributes(self) -> int:
        ...

    @property
    def IsIn(self) -> bool:
        ...

    @property
    def IsOptional(self) -> bool:
        ...

    @property
    def IsOut(self) -> bool:
        ...

    @property
    def Name(self) -> str:
        ...

    @property
    def Position(self) -> int:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def SetConstant(self, defaultValue: typing.Any) -> None:
        ...

    @overload
    def SetCustomAttribute(self, con: System.Reflection.ConstructorInfo, binaryAttribute: typing.List[int]) -> None:
        ...

    @overload
    def SetCustomAttribute(self, customBuilder: System.Reflection.Emit.CustomAttributeBuilder) -> None:
        ...

    def SetCustomAttributeCore(self, con: System.Reflection.ConstructorInfo, binaryAttribute: System.ReadOnlySpan[int]) -> None:
        """This method is protected."""
        ...


class OpCode(System.IEquatable[System_Reflection_Emit_OpCode]):
    """This class has no documentation."""

    @property
    def OperandType(self) -> int:
        """This property contains the int value of a member of the System.Reflection.Emit.OperandType enum."""
        ...

    @property
    def FlowControl(self) -> int:
        """This property contains the int value of a member of the System.Reflection.Emit.FlowControl enum."""
        ...

    @property
    def OpCodeType(self) -> int:
        """This property contains the int value of a member of the System.Reflection.Emit.OpCodeType enum."""
        ...

    @property
    def StackBehaviourPop(self) -> int:
        """This property contains the int value of a member of the System.Reflection.Emit.StackBehaviour enum."""
        ...

    @property
    def StackBehaviourPush(self) -> int:
        """This property contains the int value of a member of the System.Reflection.Emit.StackBehaviour enum."""
        ...

    @property
    def Size(self) -> int:
        ...

    @property
    def Value(self) -> int:
        ...

    @property
    def Name(self) -> str:
        ...

    @overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def Equals(self, obj: System.Reflection.Emit.OpCode) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    def ToString(self) -> str:
        ...


class Label(System.IEquatable[System_Reflection_Emit_Label]):
    """Represents a label in the instruction stream. Used in conjunction with the ILGenerator class."""

    @overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def Equals(self, obj: System.Reflection.Emit.Label) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class LocalBuilder(System.Reflection.LocalVariableInfo):
    """This class has no documentation."""

    @property
    def LocalType(self) -> typing.Type:
        ...

    @property
    def IsPinned(self) -> bool:
        ...

    @property
    def LocalIndex(self) -> int:
        ...


class ILGenerator(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    @abc.abstractmethod
    def ILOffset(self) -> int:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def BeginCatchBlock(self, exceptionType: typing.Type) -> None:
        ...

    def BeginExceptFilterBlock(self) -> None:
        ...

    def BeginExceptionBlock(self) -> System.Reflection.Emit.Label:
        ...

    def BeginFaultBlock(self) -> None:
        ...

    def BeginFinallyBlock(self) -> None:
        ...

    def BeginScope(self) -> None:
        ...

    @overload
    def DeclareLocal(self, localType: typing.Type) -> System.Reflection.Emit.LocalBuilder:
        ...

    @overload
    def DeclareLocal(self, localType: typing.Type, pinned: bool) -> System.Reflection.Emit.LocalBuilder:
        ...

    def DefineLabel(self) -> System.Reflection.Emit.Label:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, arg: int) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, arg: int) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, arg: int) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, arg: float) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, arg: float) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, arg: int) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, meth: System.Reflection.MethodInfo) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, signature: System.Reflection.Emit.SignatureHelper) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, con: System.Reflection.ConstructorInfo) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, cls: typing.Type) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, label: System.Reflection.Emit.Label) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, labels: typing.List[System.Reflection.Emit.Label]) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, field: System.Reflection.FieldInfo) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, str: str) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, local: System.Reflection.Emit.LocalBuilder) -> None:
        ...

    @overload
    def Emit(self, opcode: System.Reflection.Emit.OpCode, arg: int) -> None:
        ...

    def EmitCall(self, opcode: System.Reflection.Emit.OpCode, methodInfo: System.Reflection.MethodInfo, optionalParameterTypes: typing.List[typing.Type]) -> None:
        ...

    @overload
    def EmitCalli(self, opcode: System.Reflection.Emit.OpCode, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, parameterTypes: typing.List[typing.Type], optionalParameterTypes: typing.List[typing.Type]) -> None:
        ...

    @overload
    def EmitCalli(self, opcode: System.Reflection.Emit.OpCode, unmanagedCallConv: System.Runtime.InteropServices.CallingConvention, returnType: typing.Type, parameterTypes: typing.List[typing.Type]) -> None:
        ...

    @overload
    def EmitWriteLine(self, value: str) -> None:
        ...

    @overload
    def EmitWriteLine(self, localBuilder: System.Reflection.Emit.LocalBuilder) -> None:
        ...

    @overload
    def EmitWriteLine(self, fld: System.Reflection.FieldInfo) -> None:
        ...

    def EndExceptionBlock(self) -> None:
        ...

    def EndScope(self) -> None:
        ...

    def MarkLabel(self, loc: System.Reflection.Emit.Label) -> None:
        ...

    def ThrowException(self, excType: typing.Type) -> None:
        ...

    def UsingNamespace(self, usingNamespace: str) -> None:
        ...


class DynamicMethod(System.Reflection.MethodInfo):
    """This class has no documentation."""

    @property
    def Name(self) -> str:
        ...

    @property
    def DeclaringType(self) -> typing.Type:
        ...

    @property
    def ReflectedType(self) -> typing.Type:
        ...

    @property
    def Module(self) -> System.Reflection.Module:
        ...

    @property
    def MethodHandle(self) -> System.RuntimeMethodHandle:
        ...

    @property
    def Attributes(self) -> int:
        """This property contains the int value of a member of the System.Reflection.MethodAttributes enum."""
        ...

    @property
    def CallingConvention(self) -> int:
        """This property contains the int value of a member of the System.Reflection.CallingConventions enum."""
        ...

    @property
    def IsSecurityCritical(self) -> bool:
        ...

    @property
    def IsSecuritySafeCritical(self) -> bool:
        ...

    @property
    def IsSecurityTransparent(self) -> bool:
        ...

    @property
    def ReturnType(self) -> typing.Type:
        ...

    @property
    def ReturnParameter(self) -> System.Reflection.ParameterInfo:
        ...

    @property
    def ReturnTypeCustomAttributes(self) -> System.Reflection.ICustomAttributeProvider:
        ...

    @property
    def InitLocals(self) -> bool:
        ...

    @overload
    def __init__(self, name: str, returnType: typing.Type, parameterTypes: typing.List[typing.Type]) -> None:
        ...

    @overload
    def __init__(self, name: str, returnType: typing.Type, parameterTypes: typing.List[typing.Type], restrictedSkipVisibility: bool) -> None:
        ...

    @overload
    def __init__(self, name: str, returnType: typing.Type, parameterTypes: typing.List[typing.Type], m: System.Reflection.Module) -> None:
        ...

    @overload
    def __init__(self, name: str, returnType: typing.Type, parameterTypes: typing.List[typing.Type], m: System.Reflection.Module, skipVisibility: bool) -> None:
        ...

    @overload
    def __init__(self, name: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, parameterTypes: typing.List[typing.Type], m: System.Reflection.Module, skipVisibility: bool) -> None:
        ...

    @overload
    def __init__(self, name: str, returnType: typing.Type, parameterTypes: typing.List[typing.Type], owner: typing.Type) -> None:
        ...

    @overload
    def __init__(self, name: str, returnType: typing.Type, parameterTypes: typing.List[typing.Type], owner: typing.Type, skipVisibility: bool) -> None:
        ...

    @overload
    def __init__(self, name: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, parameterTypes: typing.List[typing.Type], owner: typing.Type, skipVisibility: bool) -> None:
        ...

    @overload
    def CreateDelegate(self, delegateType: typing.Type) -> System.Delegate:
        ...

    @overload
    def CreateDelegate(self, delegateType: typing.Type, target: typing.Any) -> System.Delegate:
        ...

    def DefineParameter(self, position: int, attributes: System.Reflection.ParameterAttributes, parameterName: str) -> System.Reflection.Emit.ParameterBuilder:
        ...

    def GetBaseDefinition(self) -> System.Reflection.MethodInfo:
        ...

    @overload
    def GetCustomAttributes(self, attributeType: typing.Type, inherit: bool) -> typing.List[System.Object]:
        ...

    @overload
    def GetCustomAttributes(self, inherit: bool) -> typing.List[System.Object]:
        ...

    def GetDynamicILInfo(self) -> System.Reflection.Emit.DynamicILInfo:
        ...

    @overload
    def GetILGenerator(self) -> System.Reflection.Emit.ILGenerator:
        ...

    @overload
    def GetILGenerator(self, streamSize: int) -> System.Reflection.Emit.ILGenerator:
        ...

    def GetMethodImplementationFlags(self) -> int:
        """:returns: This method returns the int value of a member of the System.Reflection.MethodImplAttributes enum."""
        ...

    def GetParameters(self) -> typing.List[System.Reflection.ParameterInfo]:
        ...

    def Invoke(self, obj: typing.Any, invokeAttr: System.Reflection.BindingFlags, binder: System.Reflection.Binder, parameters: typing.List[System.Object], culture: System.Globalization.CultureInfo) -> System.Object:
        ...

    def IsDefined(self, attributeType: typing.Type, inherit: bool) -> bool:
        ...

    def ToString(self) -> str:
        ...


class OperandType(System.Enum):
    """Describes the operand type of IL instruction."""

    InlineBrTarget = 0

    InlineField = 1

    InlineI = 2

    InlineI8 = 3

    InlineMethod = 4

    InlineNone = 5

    InlinePhi = 6
    """OperandType.InlinePhi has been deprecated and is not supported."""

    InlineR = 7

    InlineSig = 9

    InlineString = 10

    InlineSwitch = 11

    InlineTok = 12

    InlineType = 13

    InlineVar = 14

    ShortInlineBrTarget = 15

    ShortInlineI = 16

    ShortInlineR = 17

    ShortInlineVar = 18


class StackBehaviour(System.Enum):
    """Describes how values are pushed onto a stack or popped off a stack."""

    Pop0 = 0

    Pop1 = 1

    Pop1_pop1 = 2

    Popi = 3

    Popi_pop1 = 4

    Popi_popi = 5

    Popi_popi8 = 6

    Popi_popi_popi = 7

    Popi_popr4 = 8

    Popi_popr8 = 9

    Popref = 10

    Popref_pop1 = 11

    Popref_popi = 12

    Popref_popi_popi = 13

    Popref_popi_popi8 = 14

    Popref_popi_popr4 = 15

    Popref_popi_popr8 = 16

    Popref_popi_popref = 17

    Push0 = 18

    Push1 = 19

    Push1_push1 = 20

    Pushi = 21

    Pushi8 = 22

    Pushr4 = 23

    Pushr8 = 24

    Pushref = 25

    Varpop = 26

    Varpush = 27

    Popref_popi_pop1 = 28


class PackingSize(System.Enum):
    """This class has no documentation."""

    Unspecified = 0

    Size1 = 1

    Size2 = 2

    Size4 = 4

    Size8 = 8

    Size16 = 16

    Size32 = 32

    Size64 = 64

    Size128 = 128


class OpCodeType(System.Enum):
    """Describes the types of the IL instructions."""

    Annotation = 0
    """OpCodeType.Annotation has been deprecated and is not supported."""

    Macro = 1

    Nternal = 2

    Objmodel = 3

    Prefix = 4

    Primitive = 5


class OpCodes(System.Object):
    """
    The IL instruction opcodes supported by the
          runtime. The IL Instruction Specification describes each
          Opcode.
    """

    Nop: System.Reflection.Emit.OpCode = ...

    Break: System.Reflection.Emit.OpCode = ...

    Ldarg_0: System.Reflection.Emit.OpCode = ...

    Ldarg_1: System.Reflection.Emit.OpCode = ...

    Ldarg_2: System.Reflection.Emit.OpCode = ...

    Ldarg_3: System.Reflection.Emit.OpCode = ...

    Ldloc_0: System.Reflection.Emit.OpCode = ...

    Ldloc_1: System.Reflection.Emit.OpCode = ...

    Ldloc_2: System.Reflection.Emit.OpCode = ...

    Ldloc_3: System.Reflection.Emit.OpCode = ...

    Stloc_0: System.Reflection.Emit.OpCode = ...

    Stloc_1: System.Reflection.Emit.OpCode = ...

    Stloc_2: System.Reflection.Emit.OpCode = ...

    Stloc_3: System.Reflection.Emit.OpCode = ...

    Ldarg_S: System.Reflection.Emit.OpCode = ...

    Ldarga_S: System.Reflection.Emit.OpCode = ...

    Starg_S: System.Reflection.Emit.OpCode = ...

    Ldloc_S: System.Reflection.Emit.OpCode = ...

    Ldloca_S: System.Reflection.Emit.OpCode = ...

    Stloc_S: System.Reflection.Emit.OpCode = ...

    Ldnull: System.Reflection.Emit.OpCode = ...

    Ldc_I4_M1: System.Reflection.Emit.OpCode = ...

    Ldc_I4_0: System.Reflection.Emit.OpCode = ...

    Ldc_I4_1: System.Reflection.Emit.OpCode = ...

    Ldc_I4_2: System.Reflection.Emit.OpCode = ...

    Ldc_I4_3: System.Reflection.Emit.OpCode = ...

    Ldc_I4_4: System.Reflection.Emit.OpCode = ...

    Ldc_I4_5: System.Reflection.Emit.OpCode = ...

    Ldc_I4_6: System.Reflection.Emit.OpCode = ...

    Ldc_I4_7: System.Reflection.Emit.OpCode = ...

    Ldc_I4_8: System.Reflection.Emit.OpCode = ...

    Ldc_I4_S: System.Reflection.Emit.OpCode = ...

    Ldc_I4: System.Reflection.Emit.OpCode = ...

    Ldc_I8: System.Reflection.Emit.OpCode = ...

    Ldc_R4: System.Reflection.Emit.OpCode = ...

    Ldc_R8: System.Reflection.Emit.OpCode = ...

    Dup: System.Reflection.Emit.OpCode = ...

    Pop: System.Reflection.Emit.OpCode = ...

    Jmp: System.Reflection.Emit.OpCode = ...

    Call: System.Reflection.Emit.OpCode = ...

    Calli: System.Reflection.Emit.OpCode = ...

    Ret: System.Reflection.Emit.OpCode = ...

    Br_S: System.Reflection.Emit.OpCode = ...

    Brfalse_S: System.Reflection.Emit.OpCode = ...

    Brtrue_S: System.Reflection.Emit.OpCode = ...

    Beq_S: System.Reflection.Emit.OpCode = ...

    Bge_S: System.Reflection.Emit.OpCode = ...

    Bgt_S: System.Reflection.Emit.OpCode = ...

    Ble_S: System.Reflection.Emit.OpCode = ...

    Blt_S: System.Reflection.Emit.OpCode = ...

    Bne_Un_S: System.Reflection.Emit.OpCode = ...

    Bge_Un_S: System.Reflection.Emit.OpCode = ...

    Bgt_Un_S: System.Reflection.Emit.OpCode = ...

    Ble_Un_S: System.Reflection.Emit.OpCode = ...

    Blt_Un_S: System.Reflection.Emit.OpCode = ...

    Br: System.Reflection.Emit.OpCode = ...

    Brfalse: System.Reflection.Emit.OpCode = ...

    Brtrue: System.Reflection.Emit.OpCode = ...

    Beq: System.Reflection.Emit.OpCode = ...

    Bge: System.Reflection.Emit.OpCode = ...

    Bgt: System.Reflection.Emit.OpCode = ...

    Ble: System.Reflection.Emit.OpCode = ...

    Blt: System.Reflection.Emit.OpCode = ...

    Bne_Un: System.Reflection.Emit.OpCode = ...

    Bge_Un: System.Reflection.Emit.OpCode = ...

    Bgt_Un: System.Reflection.Emit.OpCode = ...

    Ble_Un: System.Reflection.Emit.OpCode = ...

    Blt_Un: System.Reflection.Emit.OpCode = ...

    Switch: System.Reflection.Emit.OpCode = ...

    Ldind_I1: System.Reflection.Emit.OpCode = ...

    Ldind_U1: System.Reflection.Emit.OpCode = ...

    Ldind_I2: System.Reflection.Emit.OpCode = ...

    Ldind_U2: System.Reflection.Emit.OpCode = ...

    Ldind_I4: System.Reflection.Emit.OpCode = ...

    Ldind_U4: System.Reflection.Emit.OpCode = ...

    Ldind_I8: System.Reflection.Emit.OpCode = ...

    Ldind_I: System.Reflection.Emit.OpCode = ...

    Ldind_R4: System.Reflection.Emit.OpCode = ...

    Ldind_R8: System.Reflection.Emit.OpCode = ...

    Ldind_Ref: System.Reflection.Emit.OpCode = ...

    Stind_Ref: System.Reflection.Emit.OpCode = ...

    Stind_I1: System.Reflection.Emit.OpCode = ...

    Stind_I2: System.Reflection.Emit.OpCode = ...

    Stind_I4: System.Reflection.Emit.OpCode = ...

    Stind_I8: System.Reflection.Emit.OpCode = ...

    Stind_R4: System.Reflection.Emit.OpCode = ...

    Stind_R8: System.Reflection.Emit.OpCode = ...

    Add: System.Reflection.Emit.OpCode = ...

    Sub: System.Reflection.Emit.OpCode = ...

    Mul: System.Reflection.Emit.OpCode = ...

    Div: System.Reflection.Emit.OpCode = ...

    Div_Un: System.Reflection.Emit.OpCode = ...

    Rem: System.Reflection.Emit.OpCode = ...

    Rem_Un: System.Reflection.Emit.OpCode = ...

    And: System.Reflection.Emit.OpCode = ...

    Or: System.Reflection.Emit.OpCode = ...

    Xor: System.Reflection.Emit.OpCode = ...

    Shl: System.Reflection.Emit.OpCode = ...

    Shr: System.Reflection.Emit.OpCode = ...

    Shr_Un: System.Reflection.Emit.OpCode = ...

    Neg: System.Reflection.Emit.OpCode = ...

    Not: System.Reflection.Emit.OpCode = ...

    Conv_I1: System.Reflection.Emit.OpCode = ...

    Conv_I2: System.Reflection.Emit.OpCode = ...

    Conv_I4: System.Reflection.Emit.OpCode = ...

    Conv_I8: System.Reflection.Emit.OpCode = ...

    Conv_R4: System.Reflection.Emit.OpCode = ...

    Conv_R8: System.Reflection.Emit.OpCode = ...

    Conv_U4: System.Reflection.Emit.OpCode = ...

    Conv_U8: System.Reflection.Emit.OpCode = ...

    Callvirt: System.Reflection.Emit.OpCode = ...

    Cpobj: System.Reflection.Emit.OpCode = ...

    Ldobj: System.Reflection.Emit.OpCode = ...

    Ldstr: System.Reflection.Emit.OpCode = ...

    Newobj: System.Reflection.Emit.OpCode = ...

    Castclass: System.Reflection.Emit.OpCode = ...

    Isinst: System.Reflection.Emit.OpCode = ...

    Conv_R_Un: System.Reflection.Emit.OpCode = ...

    Unbox: System.Reflection.Emit.OpCode = ...

    Throw: System.Reflection.Emit.OpCode = ...

    Ldfld: System.Reflection.Emit.OpCode = ...

    Ldflda: System.Reflection.Emit.OpCode = ...

    Stfld: System.Reflection.Emit.OpCode = ...

    Ldsfld: System.Reflection.Emit.OpCode = ...

    Ldsflda: System.Reflection.Emit.OpCode = ...

    Stsfld: System.Reflection.Emit.OpCode = ...

    Stobj: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I1_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I2_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I4_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I8_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U1_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U2_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U4_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U8_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I_Un: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U_Un: System.Reflection.Emit.OpCode = ...

    Box: System.Reflection.Emit.OpCode = ...

    Newarr: System.Reflection.Emit.OpCode = ...

    Ldlen: System.Reflection.Emit.OpCode = ...

    Ldelema: System.Reflection.Emit.OpCode = ...

    Ldelem_I1: System.Reflection.Emit.OpCode = ...

    Ldelem_U1: System.Reflection.Emit.OpCode = ...

    Ldelem_I2: System.Reflection.Emit.OpCode = ...

    Ldelem_U2: System.Reflection.Emit.OpCode = ...

    Ldelem_I4: System.Reflection.Emit.OpCode = ...

    Ldelem_U4: System.Reflection.Emit.OpCode = ...

    Ldelem_I8: System.Reflection.Emit.OpCode = ...

    Ldelem_I: System.Reflection.Emit.OpCode = ...

    Ldelem_R4: System.Reflection.Emit.OpCode = ...

    Ldelem_R8: System.Reflection.Emit.OpCode = ...

    Ldelem_Ref: System.Reflection.Emit.OpCode = ...

    Stelem_I: System.Reflection.Emit.OpCode = ...

    Stelem_I1: System.Reflection.Emit.OpCode = ...

    Stelem_I2: System.Reflection.Emit.OpCode = ...

    Stelem_I4: System.Reflection.Emit.OpCode = ...

    Stelem_I8: System.Reflection.Emit.OpCode = ...

    Stelem_R4: System.Reflection.Emit.OpCode = ...

    Stelem_R8: System.Reflection.Emit.OpCode = ...

    Stelem_Ref: System.Reflection.Emit.OpCode = ...

    Ldelem: System.Reflection.Emit.OpCode = ...

    Stelem: System.Reflection.Emit.OpCode = ...

    Unbox_Any: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I1: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U1: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I2: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U2: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I4: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U4: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I8: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U8: System.Reflection.Emit.OpCode = ...

    Refanyval: System.Reflection.Emit.OpCode = ...

    Ckfinite: System.Reflection.Emit.OpCode = ...

    Mkrefany: System.Reflection.Emit.OpCode = ...

    Ldtoken: System.Reflection.Emit.OpCode = ...

    Conv_U2: System.Reflection.Emit.OpCode = ...

    Conv_U1: System.Reflection.Emit.OpCode = ...

    Conv_I: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_I: System.Reflection.Emit.OpCode = ...

    Conv_Ovf_U: System.Reflection.Emit.OpCode = ...

    Add_Ovf: System.Reflection.Emit.OpCode = ...

    Add_Ovf_Un: System.Reflection.Emit.OpCode = ...

    Mul_Ovf: System.Reflection.Emit.OpCode = ...

    Mul_Ovf_Un: System.Reflection.Emit.OpCode = ...

    Sub_Ovf: System.Reflection.Emit.OpCode = ...

    Sub_Ovf_Un: System.Reflection.Emit.OpCode = ...

    Endfinally: System.Reflection.Emit.OpCode = ...

    Leave: System.Reflection.Emit.OpCode = ...

    Leave_S: System.Reflection.Emit.OpCode = ...

    Stind_I: System.Reflection.Emit.OpCode = ...

    Conv_U: System.Reflection.Emit.OpCode = ...

    Prefix7: System.Reflection.Emit.OpCode = ...

    Prefix6: System.Reflection.Emit.OpCode = ...

    Prefix5: System.Reflection.Emit.OpCode = ...

    Prefix4: System.Reflection.Emit.OpCode = ...

    Prefix3: System.Reflection.Emit.OpCode = ...

    Prefix2: System.Reflection.Emit.OpCode = ...

    Prefix1: System.Reflection.Emit.OpCode = ...

    Prefixref: System.Reflection.Emit.OpCode = ...

    Arglist: System.Reflection.Emit.OpCode = ...

    Ceq: System.Reflection.Emit.OpCode = ...

    Cgt: System.Reflection.Emit.OpCode = ...

    Cgt_Un: System.Reflection.Emit.OpCode = ...

    Clt: System.Reflection.Emit.OpCode = ...

    Clt_Un: System.Reflection.Emit.OpCode = ...

    Ldftn: System.Reflection.Emit.OpCode = ...

    Ldvirtftn: System.Reflection.Emit.OpCode = ...

    Ldarg: System.Reflection.Emit.OpCode = ...

    Ldarga: System.Reflection.Emit.OpCode = ...

    Starg: System.Reflection.Emit.OpCode = ...

    Ldloc: System.Reflection.Emit.OpCode = ...

    Ldloca: System.Reflection.Emit.OpCode = ...

    Stloc: System.Reflection.Emit.OpCode = ...

    Localloc: System.Reflection.Emit.OpCode = ...

    Endfilter: System.Reflection.Emit.OpCode = ...

    Unaligned: System.Reflection.Emit.OpCode = ...

    Volatile: System.Reflection.Emit.OpCode = ...

    Tailcall: System.Reflection.Emit.OpCode = ...

    Initobj: System.Reflection.Emit.OpCode = ...

    Constrained: System.Reflection.Emit.OpCode = ...

    Cpblk: System.Reflection.Emit.OpCode = ...

    Initblk: System.Reflection.Emit.OpCode = ...

    Rethrow: System.Reflection.Emit.OpCode = ...

    Sizeof: System.Reflection.Emit.OpCode = ...

    Refanytype: System.Reflection.Emit.OpCode = ...

    Readonly: System.Reflection.Emit.OpCode = ...

    @staticmethod
    def TakesSingleByteArgument(inst: System.Reflection.Emit.OpCode) -> bool:
        ...


class GenericTypeParameterBuilder(System.Reflection.TypeInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def SetBaseTypeConstraint(self, baseTypeConstraint: typing.Type) -> None:
        ...

    def SetBaseTypeConstraintCore(self, baseTypeConstraint: typing.Type) -> None:
        """This method is protected."""
        ...

    @overload
    def SetCustomAttribute(self, con: System.Reflection.ConstructorInfo, binaryAttribute: typing.List[int]) -> None:
        ...

    @overload
    def SetCustomAttribute(self, customBuilder: System.Reflection.Emit.CustomAttributeBuilder) -> None:
        ...

    def SetCustomAttributeCore(self, con: System.Reflection.ConstructorInfo, binaryAttribute: System.ReadOnlySpan[int]) -> None:
        """This method is protected."""
        ...

    def SetGenericParameterAttributes(self, genericParameterAttributes: System.Reflection.GenericParameterAttributes) -> None:
        ...

    def SetGenericParameterAttributesCore(self, genericParameterAttributes: System.Reflection.GenericParameterAttributes) -> None:
        """This method is protected."""
        ...

    def SetInterfaceConstraints(self, *interfaceConstraints: typing.Type) -> None:
        ...

    def SetInterfaceConstraintsCore(self, *interfaceConstraints: typing.Type) -> None:
        """This method is protected."""
        ...


class FieldBuilder(System.Reflection.FieldInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def SetConstant(self, defaultValue: typing.Any) -> None:
        ...

    def SetConstantCore(self, defaultValue: typing.Any) -> None:
        """This method is protected."""
        ...

    @overload
    def SetCustomAttribute(self, con: System.Reflection.ConstructorInfo, binaryAttribute: typing.List[int]) -> None:
        ...

    @overload
    def SetCustomAttribute(self, customBuilder: System.Reflection.Emit.CustomAttributeBuilder) -> None:
        ...

    def SetCustomAttributeCore(self, con: System.Reflection.ConstructorInfo, binaryAttribute: System.ReadOnlySpan[int]) -> None:
        """This method is protected."""
        ...

    def SetOffset(self, iOffset: int) -> None:
        ...

    def SetOffsetCore(self, iOffset: int) -> None:
        """This method is protected."""
        ...


class EnumBuilder(System.Reflection.TypeInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def UnderlyingField(self) -> System.Reflection.Emit.FieldBuilder:
        ...

    @property
    @abc.abstractmethod
    def UnderlyingFieldCore(self) -> System.Reflection.Emit.FieldBuilder:
        """This property is protected."""
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def CreateType(self) -> typing.Type:
        ...

    def CreateTypeInfo(self) -> System.Reflection.TypeInfo:
        ...

    def CreateTypeInfoCore(self) -> System.Reflection.TypeInfo:
        """This method is protected."""
        ...

    def DefineLiteral(self, literalName: str, literalValue: typing.Any) -> System.Reflection.Emit.FieldBuilder:
        ...

    def DefineLiteralCore(self, literalName: str, literalValue: typing.Any) -> System.Reflection.Emit.FieldBuilder:
        """This method is protected."""
        ...

    @overload
    def MakeArrayType(self) -> typing.Type:
        ...

    @overload
    def MakeArrayType(self, rank: int) -> typing.Type:
        ...

    def MakeByRefType(self) -> typing.Type:
        ...

    def MakePointerType(self) -> typing.Type:
        ...

    @overload
    def SetCustomAttribute(self, con: System.Reflection.ConstructorInfo, binaryAttribute: typing.List[int]) -> None:
        ...

    @overload
    def SetCustomAttribute(self, customBuilder: System.Reflection.Emit.CustomAttributeBuilder) -> None:
        ...

    def SetCustomAttributeCore(self, con: System.Reflection.ConstructorInfo, binaryAttribute: System.ReadOnlySpan[int]) -> None:
        """This method is protected."""
        ...


class MethodBuilder(System.Reflection.MethodInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def InitLocals(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def InitLocalsCore(self) -> bool:
        """This property is protected."""
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def DefineGenericParameters(self, *names: str) -> typing.List[System.Reflection.Emit.GenericTypeParameterBuilder]:
        ...

    def DefineGenericParametersCore(self, *names: str) -> typing.List[System.Reflection.Emit.GenericTypeParameterBuilder]:
        """This method is protected."""
        ...

    def DefineParameter(self, position: int, attributes: System.Reflection.ParameterAttributes, strParamName: str) -> System.Reflection.Emit.ParameterBuilder:
        ...

    def DefineParameterCore(self, position: int, attributes: System.Reflection.ParameterAttributes, strParamName: str) -> System.Reflection.Emit.ParameterBuilder:
        """This method is protected."""
        ...

    @overload
    def GetILGenerator(self) -> System.Reflection.Emit.ILGenerator:
        ...

    @overload
    def GetILGenerator(self, size: int) -> System.Reflection.Emit.ILGenerator:
        ...

    def GetILGeneratorCore(self, size: int) -> System.Reflection.Emit.ILGenerator:
        """This method is protected."""
        ...

    @overload
    def SetCustomAttribute(self, con: System.Reflection.ConstructorInfo, binaryAttribute: typing.List[int]) -> None:
        ...

    @overload
    def SetCustomAttribute(self, customBuilder: System.Reflection.Emit.CustomAttributeBuilder) -> None:
        ...

    def SetCustomAttributeCore(self, con: System.Reflection.ConstructorInfo, binaryAttribute: System.ReadOnlySpan[int]) -> None:
        """This method is protected."""
        ...

    def SetImplementationFlags(self, attributes: System.Reflection.MethodImplAttributes) -> None:
        ...

    def SetImplementationFlagsCore(self, attributes: System.Reflection.MethodImplAttributes) -> None:
        """This method is protected."""
        ...

    def SetParameters(self, *parameterTypes: typing.Type) -> None:
        ...

    def SetReturnType(self, returnType: typing.Type) -> None:
        ...

    def SetSignature(self, returnType: typing.Type, returnTypeRequiredCustomModifiers: typing.List[typing.Type], returnTypeOptionalCustomModifiers: typing.List[typing.Type], parameterTypes: typing.List[typing.Type], parameterTypeRequiredCustomModifiers: typing.List[typing.List[typing.Type]], parameterTypeOptionalCustomModifiers: typing.List[typing.List[typing.Type]]) -> None:
        ...

    def SetSignatureCore(self, returnType: typing.Type, returnTypeRequiredCustomModifiers: typing.List[typing.Type], returnTypeOptionalCustomModifiers: typing.List[typing.Type], parameterTypes: typing.List[typing.Type], parameterTypeRequiredCustomModifiers: typing.List[typing.List[typing.Type]], parameterTypeOptionalCustomModifiers: typing.List[typing.List[typing.Type]]) -> None:
        """This method is protected."""
        ...


class ConstructorBuilder(System.Reflection.ConstructorInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def InitLocals(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def InitLocalsCore(self) -> bool:
        """This property is protected."""
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def DefineParameter(self, iSequence: int, attributes: System.Reflection.ParameterAttributes, strParamName: str) -> System.Reflection.Emit.ParameterBuilder:
        ...

    def DefineParameterCore(self, iSequence: int, attributes: System.Reflection.ParameterAttributes, strParamName: str) -> System.Reflection.Emit.ParameterBuilder:
        """This method is protected."""
        ...

    @overload
    def GetILGenerator(self) -> System.Reflection.Emit.ILGenerator:
        ...

    @overload
    def GetILGenerator(self, streamSize: int) -> System.Reflection.Emit.ILGenerator:
        ...

    def GetILGeneratorCore(self, streamSize: int) -> System.Reflection.Emit.ILGenerator:
        """This method is protected."""
        ...

    @overload
    def SetCustomAttribute(self, con: System.Reflection.ConstructorInfo, binaryAttribute: typing.List[int]) -> None:
        ...

    @overload
    def SetCustomAttribute(self, customBuilder: System.Reflection.Emit.CustomAttributeBuilder) -> None:
        ...

    def SetCustomAttributeCore(self, con: System.Reflection.ConstructorInfo, binaryAttribute: System.ReadOnlySpan[int]) -> None:
        """This method is protected."""
        ...

    def SetImplementationFlags(self, attributes: System.Reflection.MethodImplAttributes) -> None:
        ...

    def SetImplementationFlagsCore(self, attributes: System.Reflection.MethodImplAttributes) -> None:
        """This method is protected."""
        ...


class EventBuilder(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def AddOtherMethod(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        ...

    def AddOtherMethodCore(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        """This method is protected."""
        ...

    def SetAddOnMethod(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        ...

    def SetAddOnMethodCore(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        """This method is protected."""
        ...

    @overload
    def SetCustomAttribute(self, con: System.Reflection.ConstructorInfo, binaryAttribute: typing.List[int]) -> None:
        ...

    @overload
    def SetCustomAttribute(self, customBuilder: System.Reflection.Emit.CustomAttributeBuilder) -> None:
        ...

    def SetCustomAttributeCore(self, con: System.Reflection.ConstructorInfo, binaryAttribute: System.ReadOnlySpan[int]) -> None:
        """This method is protected."""
        ...

    def SetRaiseMethod(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        ...

    def SetRaiseMethodCore(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        """This method is protected."""
        ...

    def SetRemoveOnMethod(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        ...

    def SetRemoveOnMethodCore(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        """This method is protected."""
        ...


class PropertyBuilder(System.Reflection.PropertyInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def AddOtherMethod(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        ...

    def AddOtherMethodCore(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        """This method is protected."""
        ...

    def SetConstant(self, defaultValue: typing.Any) -> None:
        ...

    def SetConstantCore(self, defaultValue: typing.Any) -> None:
        """This method is protected."""
        ...

    @overload
    def SetCustomAttribute(self, con: System.Reflection.ConstructorInfo, binaryAttribute: typing.List[int]) -> None:
        ...

    @overload
    def SetCustomAttribute(self, customBuilder: System.Reflection.Emit.CustomAttributeBuilder) -> None:
        ...

    def SetCustomAttributeCore(self, con: System.Reflection.ConstructorInfo, binaryAttribute: System.ReadOnlySpan[int]) -> None:
        """This method is protected."""
        ...

    def SetGetMethod(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        ...

    def SetGetMethodCore(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        """This method is protected."""
        ...

    def SetSetMethod(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        ...

    def SetSetMethodCore(self, mdBuilder: System.Reflection.Emit.MethodBuilder) -> None:
        """This method is protected."""
        ...


class TypeBuilder(System.Reflection.TypeInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    UnspecifiedTypeSize: int = 0

    @property
    def PackingSize(self) -> int:
        """This property contains the int value of a member of the System.Reflection.Emit.PackingSize enum."""
        ...

    @property
    @abc.abstractmethod
    def PackingSizeCore(self) -> int:
        """
        This property contains the int value of a member of the System.Reflection.Emit.PackingSize enum.
        
        This property is protected.
        """
        ...

    @property
    def Size(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def SizeCore(self) -> int:
        """This property is protected."""
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def AddInterfaceImplementation(self, interfaceType: typing.Type) -> None:
        ...

    def AddInterfaceImplementationCore(self, interfaceType: typing.Type) -> None:
        """This method is protected."""
        ...

    def CreateType(self) -> typing.Type:
        ...

    def CreateTypeInfo(self) -> System.Reflection.TypeInfo:
        ...

    def CreateTypeInfoCore(self) -> System.Reflection.TypeInfo:
        """This method is protected."""
        ...

    @overload
    def DefineConstructor(self, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, parameterTypes: typing.List[typing.Type]) -> System.Reflection.Emit.ConstructorBuilder:
        ...

    @overload
    def DefineConstructor(self, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, parameterTypes: typing.List[typing.Type], requiredCustomModifiers: typing.List[typing.List[typing.Type]], optionalCustomModifiers: typing.List[typing.List[typing.Type]]) -> System.Reflection.Emit.ConstructorBuilder:
        ...

    def DefineConstructorCore(self, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, parameterTypes: typing.List[typing.Type], requiredCustomModifiers: typing.List[typing.List[typing.Type]], optionalCustomModifiers: typing.List[typing.List[typing.Type]]) -> System.Reflection.Emit.ConstructorBuilder:
        """This method is protected."""
        ...

    def DefineDefaultConstructor(self, attributes: System.Reflection.MethodAttributes) -> System.Reflection.Emit.ConstructorBuilder:
        ...

    def DefineDefaultConstructorCore(self, attributes: System.Reflection.MethodAttributes) -> System.Reflection.Emit.ConstructorBuilder:
        """This method is protected."""
        ...

    def DefineEvent(self, name: str, attributes: System.Reflection.EventAttributes, eventtype: typing.Type) -> System.Reflection.Emit.EventBuilder:
        ...

    def DefineEventCore(self, name: str, attributes: System.Reflection.EventAttributes, eventtype: typing.Type) -> System.Reflection.Emit.EventBuilder:
        """This method is protected."""
        ...

    @overload
    def DefineField(self, fieldName: str, type: typing.Type, attributes: System.Reflection.FieldAttributes) -> System.Reflection.Emit.FieldBuilder:
        ...

    @overload
    def DefineField(self, fieldName: str, type: typing.Type, requiredCustomModifiers: typing.List[typing.Type], optionalCustomModifiers: typing.List[typing.Type], attributes: System.Reflection.FieldAttributes) -> System.Reflection.Emit.FieldBuilder:
        ...

    def DefineFieldCore(self, fieldName: str, type: typing.Type, requiredCustomModifiers: typing.List[typing.Type], optionalCustomModifiers: typing.List[typing.Type], attributes: System.Reflection.FieldAttributes) -> System.Reflection.Emit.FieldBuilder:
        """This method is protected."""
        ...

    def DefineGenericParameters(self, *names: str) -> typing.List[System.Reflection.Emit.GenericTypeParameterBuilder]:
        ...

    def DefineGenericParametersCore(self, *names: str) -> typing.List[System.Reflection.Emit.GenericTypeParameterBuilder]:
        """This method is protected."""
        ...

    def DefineInitializedData(self, name: str, data: typing.List[int], attributes: System.Reflection.FieldAttributes) -> System.Reflection.Emit.FieldBuilder:
        ...

    def DefineInitializedDataCore(self, name: str, data: typing.List[int], attributes: System.Reflection.FieldAttributes) -> System.Reflection.Emit.FieldBuilder:
        """This method is protected."""
        ...

    @overload
    def DefineMethod(self, name: str, attributes: System.Reflection.MethodAttributes) -> System.Reflection.Emit.MethodBuilder:
        ...

    @overload
    def DefineMethod(self, name: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions) -> System.Reflection.Emit.MethodBuilder:
        ...

    @overload
    def DefineMethod(self, name: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, parameterTypes: typing.List[typing.Type]) -> System.Reflection.Emit.MethodBuilder:
        ...

    @overload
    def DefineMethod(self, name: str, attributes: System.Reflection.MethodAttributes, returnType: typing.Type, parameterTypes: typing.List[typing.Type]) -> System.Reflection.Emit.MethodBuilder:
        ...

    @overload
    def DefineMethod(self, name: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, returnTypeRequiredCustomModifiers: typing.List[typing.Type], returnTypeOptionalCustomModifiers: typing.List[typing.Type], parameterTypes: typing.List[typing.Type], parameterTypeRequiredCustomModifiers: typing.List[typing.List[typing.Type]], parameterTypeOptionalCustomModifiers: typing.List[typing.List[typing.Type]]) -> System.Reflection.Emit.MethodBuilder:
        ...

    def DefineMethodCore(self, name: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, returnTypeRequiredCustomModifiers: typing.List[typing.Type], returnTypeOptionalCustomModifiers: typing.List[typing.Type], parameterTypes: typing.List[typing.Type], parameterTypeRequiredCustomModifiers: typing.List[typing.List[typing.Type]], parameterTypeOptionalCustomModifiers: typing.List[typing.List[typing.Type]]) -> System.Reflection.Emit.MethodBuilder:
        """This method is protected."""
        ...

    def DefineMethodOverride(self, methodInfoBody: System.Reflection.MethodInfo, methodInfoDeclaration: System.Reflection.MethodInfo) -> None:
        ...

    def DefineMethodOverrideCore(self, methodInfoBody: System.Reflection.MethodInfo, methodInfoDeclaration: System.Reflection.MethodInfo) -> None:
        """This method is protected."""
        ...

    @overload
    def DefineNestedType(self, name: str) -> System.Reflection.Emit.TypeBuilder:
        ...

    @overload
    def DefineNestedType(self, name: str, attr: System.Reflection.TypeAttributes) -> System.Reflection.Emit.TypeBuilder:
        ...

    @overload
    def DefineNestedType(self, name: str, attr: System.Reflection.TypeAttributes, parent: typing.Type) -> System.Reflection.Emit.TypeBuilder:
        ...

    @overload
    def DefineNestedType(self, name: str, attr: System.Reflection.TypeAttributes, parent: typing.Type, interfaces: typing.List[typing.Type]) -> System.Reflection.Emit.TypeBuilder:
        ...

    @overload
    def DefineNestedType(self, name: str, attr: System.Reflection.TypeAttributes, parent: typing.Type, typeSize: int) -> System.Reflection.Emit.TypeBuilder:
        ...

    @overload
    def DefineNestedType(self, name: str, attr: System.Reflection.TypeAttributes, parent: typing.Type, packSize: System.Reflection.Emit.PackingSize) -> System.Reflection.Emit.TypeBuilder:
        ...

    @overload
    def DefineNestedType(self, name: str, attr: System.Reflection.TypeAttributes, parent: typing.Type, packSize: System.Reflection.Emit.PackingSize, typeSize: int) -> System.Reflection.Emit.TypeBuilder:
        ...

    def DefineNestedTypeCore(self, name: str, attr: System.Reflection.TypeAttributes, parent: typing.Type, interfaces: typing.List[typing.Type], packSize: System.Reflection.Emit.PackingSize, typeSize: int) -> System.Reflection.Emit.TypeBuilder:
        """This method is protected."""
        ...

    @overload
    def DefinePInvokeMethod(self, name: str, dllName: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, parameterTypes: typing.List[typing.Type], nativeCallConv: System.Runtime.InteropServices.CallingConvention, nativeCharSet: System.Runtime.InteropServices.CharSet) -> System.Reflection.Emit.MethodBuilder:
        ...

    @overload
    def DefinePInvokeMethod(self, name: str, dllName: str, entryName: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, parameterTypes: typing.List[typing.Type], nativeCallConv: System.Runtime.InteropServices.CallingConvention, nativeCharSet: System.Runtime.InteropServices.CharSet) -> System.Reflection.Emit.MethodBuilder:
        ...

    @overload
    def DefinePInvokeMethod(self, name: str, dllName: str, entryName: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, returnTypeRequiredCustomModifiers: typing.List[typing.Type], returnTypeOptionalCustomModifiers: typing.List[typing.Type], parameterTypes: typing.List[typing.Type], parameterTypeRequiredCustomModifiers: typing.List[typing.List[typing.Type]], parameterTypeOptionalCustomModifiers: typing.List[typing.List[typing.Type]], nativeCallConv: System.Runtime.InteropServices.CallingConvention, nativeCharSet: System.Runtime.InteropServices.CharSet) -> System.Reflection.Emit.MethodBuilder:
        ...

    def DefinePInvokeMethodCore(self, name: str, dllName: str, entryName: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, returnTypeRequiredCustomModifiers: typing.List[typing.Type], returnTypeOptionalCustomModifiers: typing.List[typing.Type], parameterTypes: typing.List[typing.Type], parameterTypeRequiredCustomModifiers: typing.List[typing.List[typing.Type]], parameterTypeOptionalCustomModifiers: typing.List[typing.List[typing.Type]], nativeCallConv: System.Runtime.InteropServices.CallingConvention, nativeCharSet: System.Runtime.InteropServices.CharSet) -> System.Reflection.Emit.MethodBuilder:
        """This method is protected."""
        ...

    @overload
    def DefineProperty(self, name: str, attributes: System.Reflection.PropertyAttributes, returnType: typing.Type, parameterTypes: typing.List[typing.Type]) -> System.Reflection.Emit.PropertyBuilder:
        ...

    @overload
    def DefineProperty(self, name: str, attributes: System.Reflection.PropertyAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, parameterTypes: typing.List[typing.Type]) -> System.Reflection.Emit.PropertyBuilder:
        ...

    @overload
    def DefineProperty(self, name: str, attributes: System.Reflection.PropertyAttributes, returnType: typing.Type, returnTypeRequiredCustomModifiers: typing.List[typing.Type], returnTypeOptionalCustomModifiers: typing.List[typing.Type], parameterTypes: typing.List[typing.Type], parameterTypeRequiredCustomModifiers: typing.List[typing.List[typing.Type]], parameterTypeOptionalCustomModifiers: typing.List[typing.List[typing.Type]]) -> System.Reflection.Emit.PropertyBuilder:
        ...

    @overload
    def DefineProperty(self, name: str, attributes: System.Reflection.PropertyAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, returnTypeRequiredCustomModifiers: typing.List[typing.Type], returnTypeOptionalCustomModifiers: typing.List[typing.Type], parameterTypes: typing.List[typing.Type], parameterTypeRequiredCustomModifiers: typing.List[typing.List[typing.Type]], parameterTypeOptionalCustomModifiers: typing.List[typing.List[typing.Type]]) -> System.Reflection.Emit.PropertyBuilder:
        ...

    def DefinePropertyCore(self, name: str, attributes: System.Reflection.PropertyAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, returnTypeRequiredCustomModifiers: typing.List[typing.Type], returnTypeOptionalCustomModifiers: typing.List[typing.Type], parameterTypes: typing.List[typing.Type], parameterTypeRequiredCustomModifiers: typing.List[typing.List[typing.Type]], parameterTypeOptionalCustomModifiers: typing.List[typing.List[typing.Type]]) -> System.Reflection.Emit.PropertyBuilder:
        """This method is protected."""
        ...

    def DefineTypeInitializer(self) -> System.Reflection.Emit.ConstructorBuilder:
        ...

    def DefineTypeInitializerCore(self) -> System.Reflection.Emit.ConstructorBuilder:
        """This method is protected."""
        ...

    def DefineUninitializedData(self, name: str, size: int, attributes: System.Reflection.FieldAttributes) -> System.Reflection.Emit.FieldBuilder:
        ...

    def DefineUninitializedDataCore(self, name: str, size: int, attributes: System.Reflection.FieldAttributes) -> System.Reflection.Emit.FieldBuilder:
        """This method is protected."""
        ...

    @staticmethod
    def GetConstructor(type: typing.Type, constructor: System.Reflection.ConstructorInfo) -> System.Reflection.ConstructorInfo:
        ...

    @staticmethod
    def GetField(type: typing.Type, field: System.Reflection.FieldInfo) -> System.Reflection.FieldInfo:
        ...

    @staticmethod
    def GetMethod(type: typing.Type, method: System.Reflection.MethodInfo) -> System.Reflection.MethodInfo:
        ...

    def IsCreated(self) -> bool:
        ...

    def IsCreatedCore(self) -> bool:
        """This method is protected."""
        ...

    @overload
    def MakeArrayType(self) -> typing.Type:
        ...

    @overload
    def MakeArrayType(self, rank: int) -> typing.Type:
        ...

    def MakeByRefType(self) -> typing.Type:
        ...

    def MakeGenericType(self, *typeArguments: typing.Type) -> typing.Type:
        ...

    def MakePointerType(self) -> typing.Type:
        ...

    @overload
    def SetCustomAttribute(self, con: System.Reflection.ConstructorInfo, binaryAttribute: typing.List[int]) -> None:
        ...

    @overload
    def SetCustomAttribute(self, customBuilder: System.Reflection.Emit.CustomAttributeBuilder) -> None:
        ...

    def SetCustomAttributeCore(self, con: System.Reflection.ConstructorInfo, binaryAttribute: System.ReadOnlySpan[int]) -> None:
        """This method is protected."""
        ...

    def SetParent(self, parent: typing.Type) -> None:
        ...

    def SetParentCore(self, parent: typing.Type) -> None:
        """This method is protected."""
        ...


class ModuleBuilder(System.Reflection.Module, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __init__(self) -> None:
        """This method is protected."""
        ...

    def CreateGlobalFunctions(self) -> None:
        ...

    def CreateGlobalFunctionsCore(self) -> None:
        """This method is protected."""
        ...

    def DefineEnum(self, name: str, visibility: System.Reflection.TypeAttributes, underlyingType: typing.Type) -> System.Reflection.Emit.EnumBuilder:
        ...

    def DefineEnumCore(self, name: str, visibility: System.Reflection.TypeAttributes, underlyingType: typing.Type) -> System.Reflection.Emit.EnumBuilder:
        """This method is protected."""
        ...

    @overload
    def DefineGlobalMethod(self, name: str, attributes: System.Reflection.MethodAttributes, returnType: typing.Type, parameterTypes: typing.List[typing.Type]) -> System.Reflection.Emit.MethodBuilder:
        ...

    @overload
    def DefineGlobalMethod(self, name: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, parameterTypes: typing.List[typing.Type]) -> System.Reflection.Emit.MethodBuilder:
        ...

    @overload
    def DefineGlobalMethod(self, name: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, requiredReturnTypeCustomModifiers: typing.List[typing.Type], optionalReturnTypeCustomModifiers: typing.List[typing.Type], parameterTypes: typing.List[typing.Type], requiredParameterTypeCustomModifiers: typing.List[typing.List[typing.Type]], optionalParameterTypeCustomModifiers: typing.List[typing.List[typing.Type]]) -> System.Reflection.Emit.MethodBuilder:
        ...

    def DefineGlobalMethodCore(self, name: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, requiredReturnTypeCustomModifiers: typing.List[typing.Type], optionalReturnTypeCustomModifiers: typing.List[typing.Type], parameterTypes: typing.List[typing.Type], requiredParameterTypeCustomModifiers: typing.List[typing.List[typing.Type]], optionalParameterTypeCustomModifiers: typing.List[typing.List[typing.Type]]) -> System.Reflection.Emit.MethodBuilder:
        """This method is protected."""
        ...

    def DefineInitializedData(self, name: str, data: typing.List[int], attributes: System.Reflection.FieldAttributes) -> System.Reflection.Emit.FieldBuilder:
        ...

    def DefineInitializedDataCore(self, name: str, data: typing.List[int], attributes: System.Reflection.FieldAttributes) -> System.Reflection.Emit.FieldBuilder:
        """This method is protected."""
        ...

    @overload
    def DefinePInvokeMethod(self, name: str, dllName: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, parameterTypes: typing.List[typing.Type], nativeCallConv: System.Runtime.InteropServices.CallingConvention, nativeCharSet: System.Runtime.InteropServices.CharSet) -> System.Reflection.Emit.MethodBuilder:
        ...

    @overload
    def DefinePInvokeMethod(self, name: str, dllName: str, entryName: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, parameterTypes: typing.List[typing.Type], nativeCallConv: System.Runtime.InteropServices.CallingConvention, nativeCharSet: System.Runtime.InteropServices.CharSet) -> System.Reflection.Emit.MethodBuilder:
        ...

    def DefinePInvokeMethodCore(self, name: str, dllName: str, entryName: str, attributes: System.Reflection.MethodAttributes, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, parameterTypes: typing.List[typing.Type], nativeCallConv: System.Runtime.InteropServices.CallingConvention, nativeCharSet: System.Runtime.InteropServices.CharSet) -> System.Reflection.Emit.MethodBuilder:
        """This method is protected."""
        ...

    @overload
    def DefineType(self, name: str) -> System.Reflection.Emit.TypeBuilder:
        ...

    @overload
    def DefineType(self, name: str, attr: System.Reflection.TypeAttributes) -> System.Reflection.Emit.TypeBuilder:
        ...

    @overload
    def DefineType(self, name: str, attr: System.Reflection.TypeAttributes, parent: typing.Type) -> System.Reflection.Emit.TypeBuilder:
        ...

    @overload
    def DefineType(self, name: str, attr: System.Reflection.TypeAttributes, parent: typing.Type, interfaces: typing.List[typing.Type]) -> System.Reflection.Emit.TypeBuilder:
        ...

    @overload
    def DefineType(self, name: str, attr: System.Reflection.TypeAttributes, parent: typing.Type, typesize: int) -> System.Reflection.Emit.TypeBuilder:
        ...

    @overload
    def DefineType(self, name: str, attr: System.Reflection.TypeAttributes, parent: typing.Type, packsize: System.Reflection.Emit.PackingSize) -> System.Reflection.Emit.TypeBuilder:
        ...

    @overload
    def DefineType(self, name: str, attr: System.Reflection.TypeAttributes, parent: typing.Type, packingSize: System.Reflection.Emit.PackingSize, typesize: int) -> System.Reflection.Emit.TypeBuilder:
        ...

    def DefineTypeCore(self, name: str, attr: System.Reflection.TypeAttributes, parent: typing.Type, interfaces: typing.List[typing.Type], packingSize: System.Reflection.Emit.PackingSize, typesize: int) -> System.Reflection.Emit.TypeBuilder:
        """This method is protected."""
        ...

    def DefineUninitializedData(self, name: str, size: int, attributes: System.Reflection.FieldAttributes) -> System.Reflection.Emit.FieldBuilder:
        ...

    def DefineUninitializedDataCore(self, name: str, size: int, attributes: System.Reflection.FieldAttributes) -> System.Reflection.Emit.FieldBuilder:
        """This method is protected."""
        ...

    def GetArrayMethod(self, arrayClass: typing.Type, methodName: str, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, parameterTypes: typing.List[typing.Type]) -> System.Reflection.MethodInfo:
        ...

    def GetArrayMethodCore(self, arrayClass: typing.Type, methodName: str, callingConvention: System.Reflection.CallingConventions, returnType: typing.Type, parameterTypes: typing.List[typing.Type]) -> System.Reflection.MethodInfo:
        """This method is protected."""
        ...

    def GetFieldMetadataToken(self, field: System.Reflection.FieldInfo) -> int:
        ...

    @overload
    def GetMethodMetadataToken(self, method: System.Reflection.MethodInfo) -> int:
        ...

    @overload
    def GetMethodMetadataToken(self, constructor: System.Reflection.ConstructorInfo) -> int:
        ...

    def GetSignatureMetadataToken(self, signature: System.Reflection.Emit.SignatureHelper) -> int:
        ...

    def GetStringMetadataToken(self, stringConstant: str) -> int:
        ...

    def GetTypeMetadataToken(self, type: typing.Type) -> int:
        ...

    @overload
    def SetCustomAttribute(self, con: System.Reflection.ConstructorInfo, binaryAttribute: typing.List[int]) -> None:
        ...

    @overload
    def SetCustomAttribute(self, customBuilder: System.Reflection.Emit.CustomAttributeBuilder) -> None:
        ...

    def SetCustomAttributeCore(self, con: System.Reflection.ConstructorInfo, binaryAttribute: System.ReadOnlySpan[int]) -> None:
        """This method is protected."""
        ...


class FlowControl(System.Enum):
    """Describes how an instruction alters the flow of control."""

    Branch = 0

    Break = 1

    Call = 2

    Cond_Branch = 3

    Meta = 4

    Next = 5

    Phi = 6
    """FlowControl.Phi has been deprecated and is not supported."""

    Return = 7

    Throw = 8


class AssemblyBuilderAccess(System.Enum):
    """This class has no documentation."""

    Run = 1

    RunAndCollect = ...


class AssemblyBuilder(System.Reflection.Assembly, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def CodeBase(self) -> str:
        """Assembly.CodeBase and Assembly.EscapedCodeBase are only included for .NET Framework compatibility. Use Assembly.Location instead."""
        warnings.warn("Assembly.CodeBase and Assembly.EscapedCodeBase are only included for .NET Framework compatibility. Use Assembly.Location instead.", DeprecationWarning)

    @property
    def Location(self) -> str:
        ...

    @property
    def EntryPoint(self) -> System.Reflection.MethodInfo:
        ...

    @property
    def IsDynamic(self) -> bool:
        ...

    def __init__(self) -> None:
        """This method is protected."""
        ...

    @staticmethod
    @overload
    def DefineDynamicAssembly(name: System.Reflection.AssemblyName, access: System.Reflection.Emit.AssemblyBuilderAccess) -> System.Reflection.Emit.AssemblyBuilder:
        ...

    @staticmethod
    @overload
    def DefineDynamicAssembly(name: System.Reflection.AssemblyName, access: System.Reflection.Emit.AssemblyBuilderAccess, assemblyAttributes: System.Collections.Generic.IEnumerable[System.Reflection.Emit.CustomAttributeBuilder]) -> System.Reflection.Emit.AssemblyBuilder:
        ...

    def DefineDynamicModule(self, name: str) -> System.Reflection.Emit.ModuleBuilder:
        ...

    def DefineDynamicModuleCore(self, name: str) -> System.Reflection.Emit.ModuleBuilder:
        """This method is protected."""
        ...

    def GetDynamicModule(self, name: str) -> System.Reflection.Emit.ModuleBuilder:
        ...

    def GetDynamicModuleCore(self, name: str) -> System.Reflection.Emit.ModuleBuilder:
        """This method is protected."""
        ...

    def GetExportedTypes(self) -> typing.List[typing.Type]:
        ...

    def GetFile(self, name: str) -> System.IO.FileStream:
        ...

    def GetFiles(self, getResourceModules: bool) -> typing.List[System.IO.FileStream]:
        ...

    def GetManifestResourceInfo(self, resourceName: str) -> System.Reflection.ManifestResourceInfo:
        ...

    def GetManifestResourceNames(self) -> typing.List[str]:
        ...

    @overload
    def GetManifestResourceStream(self, name: str) -> System.IO.Stream:
        ...

    @overload
    def GetManifestResourceStream(self, type: typing.Type, name: str) -> System.IO.Stream:
        ...

    @overload
    def SetCustomAttribute(self, con: System.Reflection.ConstructorInfo, binaryAttribute: typing.List[int]) -> None:
        ...

    @overload
    def SetCustomAttribute(self, customBuilder: System.Reflection.Emit.CustomAttributeBuilder) -> None:
        ...

    def SetCustomAttributeCore(self, con: System.Reflection.ConstructorInfo, binaryAttribute: System.ReadOnlySpan[int]) -> None:
        """This method is protected."""
        ...


class PEFileKinds(System.Enum):
    """This class has no documentation."""

    Dll = ...

    ConsoleApplication = ...

    WindowApplication = ...


