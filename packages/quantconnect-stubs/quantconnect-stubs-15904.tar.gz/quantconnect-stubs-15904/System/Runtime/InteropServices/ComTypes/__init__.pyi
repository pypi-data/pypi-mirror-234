from typing import overload
import abc

import System
import System.Runtime.InteropServices.ComTypes


class IConnectionPointContainer(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IEnumVARIANT(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class ITypeInfo(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class ITypeInfo2(System.Runtime.InteropServices.ComTypes.ITypeInfo, metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IConnectionPoint(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IEnumMoniker(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class SYSKIND(System.Enum):
    """This class has no documentation."""

    SYS_WIN16 = 0

    SYS_WIN32 = ...

    SYS_MAC = ...

    SYS_WIN64 = ...


class LIBFLAGS(System.Enum):
    """This class has no documentation."""

    LIBFLAG_FRESTRICTED = ...

    LIBFLAG_FCONTROL = ...

    LIBFLAG_FHIDDEN = ...

    LIBFLAG_FHASDISKIMAGE = ...


class TYPELIBATTR:
    """This class has no documentation."""

    @property
    def guid(self) -> System.Guid:
        ...

    @property
    def lcid(self) -> int:
        ...

    @property
    def syskind(self) -> System.Runtime.InteropServices.ComTypes.SYSKIND:
        ...

    @property
    def wMajorVerNum(self) -> int:
        ...

    @property
    def wMinorVerNum(self) -> int:
        ...

    @property
    def wLibFlags(self) -> System.Runtime.InteropServices.ComTypes.LIBFLAGS:
        ...


class ITypeLib(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class FILETIME:
    """This class has no documentation."""

    @property
    def dwLowDateTime(self) -> int:
        ...

    @property
    def dwHighDateTime(self) -> int:
        ...


class STATSTG:
    """This class has no documentation."""

    @property
    def pwcsName(self) -> str:
        ...

    @property
    def type(self) -> int:
        ...

    @property
    def cbSize(self) -> int:
        ...

    @property
    def mtime(self) -> System.Runtime.InteropServices.ComTypes.FILETIME:
        ...

    @property
    def ctime(self) -> System.Runtime.InteropServices.ComTypes.FILETIME:
        ...

    @property
    def atime(self) -> System.Runtime.InteropServices.ComTypes.FILETIME:
        ...

    @property
    def grfMode(self) -> int:
        ...

    @property
    def grfLocksSupported(self) -> int:
        ...

    @property
    def clsid(self) -> System.Guid:
        ...

    @property
    def grfStateBits(self) -> int:
        ...

    @property
    def reserved(self) -> int:
        ...


class IStream(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IRunningObjectTable(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class BIND_OPTS:
    """This class has no documentation."""

    @property
    def cbStruct(self) -> int:
        ...

    @property
    def grfFlags(self) -> int:
        ...

    @property
    def grfMode(self) -> int:
        ...

    @property
    def dwTickCountDeadline(self) -> int:
        ...


class IBindCtx(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IEnumConnectionPoints(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class DESCKIND(System.Enum):
    """This class has no documentation."""

    DESCKIND_NONE = 0

    DESCKIND_FUNCDESC = ...

    DESCKIND_VARDESC = ...

    DESCKIND_TYPECOMP = ...

    DESCKIND_IMPLICITAPPOBJ = ...

    DESCKIND_MAX = ...


class BINDPTR:
    """This class has no documentation."""

    @property
    def lpfuncdesc(self) -> System.IntPtr:
        ...

    @property
    def lpvardesc(self) -> System.IntPtr:
        ...

    @property
    def lptcomp(self) -> System.IntPtr:
        ...


class ITypeComp(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class CONNECTDATA:
    """This class has no documentation."""

    @property
    def pUnk(self) -> System.Object:
        ...

    @property
    def dwCookie(self) -> int:
        ...


class IEnumConnections(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class TYPEKIND(System.Enum):
    """This class has no documentation."""

    TKIND_ENUM = 0

    TKIND_RECORD = ...

    TKIND_MODULE = ...

    TKIND_INTERFACE = ...

    TKIND_DISPATCH = ...

    TKIND_COCLASS = ...

    TKIND_ALIAS = ...

    TKIND_UNION = ...

    TKIND_MAX = ...


class TYPEFLAGS(System.Enum):
    """This class has no documentation."""

    TYPEFLAG_FAPPOBJECT = ...

    TYPEFLAG_FCANCREATE = ...

    TYPEFLAG_FLICENSED = ...

    TYPEFLAG_FPREDECLID = ...

    TYPEFLAG_FHIDDEN = ...

    TYPEFLAG_FCONTROL = ...

    TYPEFLAG_FDUAL = ...

    TYPEFLAG_FNONEXTENSIBLE = ...

    TYPEFLAG_FOLEAUTOMATION = ...

    TYPEFLAG_FRESTRICTED = ...

    TYPEFLAG_FAGGREGATABLE = ...

    TYPEFLAG_FREPLACEABLE = ...

    TYPEFLAG_FDISPATCHABLE = ...

    TYPEFLAG_FREVERSEBIND = ...

    TYPEFLAG_FPROXY = ...


class IMPLTYPEFLAGS(System.Enum):
    """This class has no documentation."""

    IMPLTYPEFLAG_FDEFAULT = ...

    IMPLTYPEFLAG_FSOURCE = ...

    IMPLTYPEFLAG_FRESTRICTED = ...

    IMPLTYPEFLAG_FDEFAULTVTABLE = ...


class TYPEDESC:
    """This class has no documentation."""

    @property
    def lpValue(self) -> System.IntPtr:
        ...

    @property
    def vt(self) -> int:
        ...


class IDLFLAG(System.Enum):
    """This class has no documentation."""

    IDLFLAG_NONE = ...

    IDLFLAG_FIN = ...

    IDLFLAG_FOUT = ...

    IDLFLAG_FLCID = ...

    IDLFLAG_FRETVAL = ...


class IDLDESC:
    """This class has no documentation."""

    @property
    def dwReserved(self) -> System.IntPtr:
        ...

    @property
    def wIDLFlags(self) -> System.Runtime.InteropServices.ComTypes.IDLFLAG:
        ...


class TYPEATTR:
    """This class has no documentation."""

    MEMBER_ID_NIL: int = ...

    @property
    def guid(self) -> System.Guid:
        ...

    @property
    def lcid(self) -> int:
        ...

    @property
    def dwReserved(self) -> int:
        ...

    @property
    def memidConstructor(self) -> int:
        ...

    @property
    def memidDestructor(self) -> int:
        ...

    @property
    def lpstrSchema(self) -> System.IntPtr:
        ...

    @property
    def cbSizeInstance(self) -> int:
        ...

    @property
    def typekind(self) -> System.Runtime.InteropServices.ComTypes.TYPEKIND:
        ...

    @property
    def cFuncs(self) -> int:
        ...

    @property
    def cVars(self) -> int:
        ...

    @property
    def cImplTypes(self) -> int:
        ...

    @property
    def cbSizeVft(self) -> int:
        ...

    @property
    def cbAlignment(self) -> int:
        ...

    @property
    def wTypeFlags(self) -> System.Runtime.InteropServices.ComTypes.TYPEFLAGS:
        ...

    @property
    def wMajorVerNum(self) -> int:
        ...

    @property
    def wMinorVerNum(self) -> int:
        ...

    @property
    def tdescAlias(self) -> System.Runtime.InteropServices.ComTypes.TYPEDESC:
        ...

    @property
    def idldescType(self) -> System.Runtime.InteropServices.ComTypes.IDLDESC:
        ...


class FUNCKIND(System.Enum):
    """This class has no documentation."""

    FUNC_VIRTUAL = 0

    FUNC_PUREVIRTUAL = 1

    FUNC_NONVIRTUAL = 2

    FUNC_STATIC = 3

    FUNC_DISPATCH = 4


class INVOKEKIND(System.Enum):
    """This class has no documentation."""

    INVOKE_FUNC = ...

    INVOKE_PROPERTYGET = ...

    INVOKE_PROPERTYPUT = ...

    INVOKE_PROPERTYPUTREF = ...


class CALLCONV(System.Enum):
    """This class has no documentation."""

    CC_CDECL = 1

    CC_MSCPASCAL = 2

    CC_PASCAL = ...

    CC_MACPASCAL = 3

    CC_STDCALL = 4

    CC_RESERVED = 5

    CC_SYSCALL = 6

    CC_MPWCDECL = 7

    CC_MPWPASCAL = 8

    CC_MAX = 9


class PARAMFLAG(System.Enum):
    """This class has no documentation."""

    PARAMFLAG_NONE = 0

    PARAMFLAG_FIN = ...

    PARAMFLAG_FOUT = ...

    PARAMFLAG_FLCID = ...

    PARAMFLAG_FRETVAL = ...

    PARAMFLAG_FOPT = ...

    PARAMFLAG_FHASDEFAULT = ...

    PARAMFLAG_FHASCUSTDATA = ...


class PARAMDESC:
    """This class has no documentation."""

    @property
    def lpVarValue(self) -> System.IntPtr:
        ...

    @property
    def wParamFlags(self) -> System.Runtime.InteropServices.ComTypes.PARAMFLAG:
        ...


class ELEMDESC:
    """This class has no documentation."""

    class DESCUNION:
        """This class has no documentation."""

        @property
        def idldesc(self) -> System.Runtime.InteropServices.ComTypes.IDLDESC:
            ...

        @property
        def paramdesc(self) -> System.Runtime.InteropServices.ComTypes.PARAMDESC:
            ...

    @property
    def tdesc(self) -> System.Runtime.InteropServices.ComTypes.TYPEDESC:
        ...

    @property
    def desc(self) -> System.Runtime.InteropServices.ComTypes.ELEMDESC.DESCUNION:
        ...


class FUNCDESC:
    """This class has no documentation."""

    @property
    def memid(self) -> int:
        ...

    @property
    def lprgscode(self) -> System.IntPtr:
        ...

    @property
    def lprgelemdescParam(self) -> System.IntPtr:
        ...

    @property
    def funckind(self) -> System.Runtime.InteropServices.ComTypes.FUNCKIND:
        ...

    @property
    def invkind(self) -> System.Runtime.InteropServices.ComTypes.INVOKEKIND:
        ...

    @property
    def callconv(self) -> System.Runtime.InteropServices.ComTypes.CALLCONV:
        ...

    @property
    def cParams(self) -> int:
        ...

    @property
    def cParamsOpt(self) -> int:
        ...

    @property
    def oVft(self) -> int:
        ...

    @property
    def cScodes(self) -> int:
        ...

    @property
    def elemdescFunc(self) -> System.Runtime.InteropServices.ComTypes.ELEMDESC:
        ...

    @property
    def wFuncFlags(self) -> int:
        ...


class VARKIND(System.Enum):
    """This class has no documentation."""

    VAR_PERINSTANCE = ...

    VAR_STATIC = ...

    VAR_CONST = ...

    VAR_DISPATCH = ...


class VARDESC:
    """This class has no documentation."""

    class DESCUNION:
        """This class has no documentation."""

        @property
        def oInst(self) -> int:
            ...

        @property
        def lpvarValue(self) -> System.IntPtr:
            ...

    @property
    def memid(self) -> int:
        ...

    @property
    def lpstrSchema(self) -> str:
        ...

    @property
    def desc(self) -> System.Runtime.InteropServices.ComTypes.VARDESC.DESCUNION:
        ...

    @property
    def elemdescVar(self) -> System.Runtime.InteropServices.ComTypes.ELEMDESC:
        ...

    @property
    def wVarFlags(self) -> int:
        ...

    @property
    def varkind(self) -> System.Runtime.InteropServices.ComTypes.VARKIND:
        ...


class DISPPARAMS:
    """This class has no documentation."""

    @property
    def rgvarg(self) -> System.IntPtr:
        ...

    @property
    def rgdispidNamedArgs(self) -> System.IntPtr:
        ...

    @property
    def cArgs(self) -> int:
        ...

    @property
    def cNamedArgs(self) -> int:
        ...


class EXCEPINFO:
    """This class has no documentation."""

    @property
    def wCode(self) -> int:
        ...

    @property
    def wReserved(self) -> int:
        ...

    @property
    def bstrSource(self) -> str:
        ...

    @property
    def bstrDescription(self) -> str:
        ...

    @property
    def bstrHelpFile(self) -> str:
        ...

    @property
    def dwHelpContext(self) -> int:
        ...

    @property
    def pvReserved(self) -> System.IntPtr:
        ...

    @property
    def pfnDeferredFillIn(self) -> System.IntPtr:
        ...

    @property
    def scode(self) -> int:
        ...


class FUNCFLAGS(System.Enum):
    """This class has no documentation."""

    FUNCFLAG_FRESTRICTED = ...

    FUNCFLAG_FSOURCE = ...

    FUNCFLAG_FBINDABLE = ...

    FUNCFLAG_FREQUESTEDIT = ...

    FUNCFLAG_FDISPLAYBIND = ...

    FUNCFLAG_FDEFAULTBIND = ...

    FUNCFLAG_FHIDDEN = ...

    FUNCFLAG_FUSESGETLASTERROR = ...

    FUNCFLAG_FDEFAULTCOLLELEM = ...

    FUNCFLAG_FUIDEFAULT = ...

    FUNCFLAG_FNONBROWSABLE = ...

    FUNCFLAG_FREPLACEABLE = ...

    FUNCFLAG_FIMMEDIATEBIND = ...


class VARFLAGS(System.Enum):
    """This class has no documentation."""

    VARFLAG_FREADONLY = ...

    VARFLAG_FSOURCE = ...

    VARFLAG_FBINDABLE = ...

    VARFLAG_FREQUESTEDIT = ...

    VARFLAG_FDISPLAYBIND = ...

    VARFLAG_FDEFAULTBIND = ...

    VARFLAG_FHIDDEN = ...

    VARFLAG_FRESTRICTED = ...

    VARFLAG_FDEFAULTCOLLELEM = ...

    VARFLAG_FUIDEFAULT = ...

    VARFLAG_FNONBROWSABLE = ...

    VARFLAG_FREPLACEABLE = ...

    VARFLAG_FIMMEDIATEBIND = ...


class ITypeLib2(System.Runtime.InteropServices.ComTypes.ITypeLib, metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IEnumString(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IPersistFile(metaclass=abc.ABCMeta):
    """This class has no documentation."""


class IMoniker(metaclass=abc.ABCMeta):
    """This class has no documentation."""


