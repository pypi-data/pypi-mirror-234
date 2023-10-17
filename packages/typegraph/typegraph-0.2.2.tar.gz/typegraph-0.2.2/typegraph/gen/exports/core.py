from ..intrinsics import _clamp, _decode_utf8, _encode_utf8, _list_canon_lower, _load, _store
from ..types import Err, Ok, Result
import ctypes
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union
import wasmtime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .. import Root

@dataclass
class Error:
    stack: List[str]

@dataclass
class Cors:
    allow_origin: List[str]
    allow_headers: List[str]
    expose_headers: List[str]
    allow_methods: List[str]
    allow_credentials: bool
    max_age_sec: Optional[int]

@dataclass
class AuthProtocolOauth2:
    pass

@dataclass
class AuthProtocolJwt:
    pass

@dataclass
class AuthProtocolBasic:
    pass

AuthProtocol = Union[AuthProtocolOauth2, AuthProtocolJwt, AuthProtocolBasic]

@dataclass
class Auth:
    name: str
    protocol: AuthProtocol
    auth_data: List[Tuple[str, str]]

@dataclass
class Rate:
    window_limit: int
    window_sec: int
    query_limit: int
    context_identifier: Optional[str]
    local_excess: int

@dataclass
class TypegraphInitParams:
    name: str
    dynamic: Optional[bool]
    path: str
    prefix: Optional[str]
    cors: Cors
    auths: List[Auth]
    rate: Optional[Rate]

TypeId = int
@dataclass
class TypeBase:
    name: Optional[str]
    runtime_config: Optional[List[Tuple[str, str]]]
    as_id: bool

@dataclass
class TypeWithInjection:
    tpe: TypeId
    injection: str

@dataclass
class TypeProxy:
    name: str
    extras: List[Tuple[str, str]]

@dataclass
class TypeInteger:
    min: Optional[int]
    max: Optional[int]
    exclusive_minimum: Optional[int]
    exclusive_maximum: Optional[int]
    multiple_of: Optional[int]
    enumeration: Optional[List[int]]

@dataclass
class TypeFloat:
    min: Optional[float]
    max: Optional[float]
    exclusive_minimum: Optional[float]
    exclusive_maximum: Optional[float]
    multiple_of: Optional[float]
    enumeration: Optional[List[float]]

@dataclass
class TypeString:
    min: Optional[int]
    max: Optional[int]
    format: Optional[str]
    pattern: Optional[str]
    enumeration: Optional[List[str]]

@dataclass
class TypeFile:
    min: Optional[int]
    max: Optional[int]
    allow: Optional[List[str]]

@dataclass
class TypeArray:
    of: TypeId
    min: Optional[int]
    max: Optional[int]
    unique_items: Optional[bool]

@dataclass
class TypeOptional:
    of: TypeId
    default_item: Optional[str]

@dataclass
class TypeUnion:
    variants: List[TypeId]

@dataclass
class TypeEither:
    variants: List[TypeId]

@dataclass
class TypeStruct:
    props: List[Tuple[str, TypeId]]
    additional_props: bool
    min: Optional[int]
    max: Optional[int]
    enumeration: Optional[List[str]]

PolicyId = int
@dataclass
class PolicyPerEffect:
    read: Optional[PolicyId]
    create: Optional[PolicyId]
    update: Optional[PolicyId]
    delete: Optional[PolicyId]

@dataclass
class PolicySpecSimple:
    value: PolicyId

@dataclass
class PolicySpecPerEffect:
    value: PolicyPerEffect

PolicySpec = Union[PolicySpecSimple, PolicySpecPerEffect]

@dataclass
class TypePolicy:
    tpe: TypeId
    chain: List[PolicySpec]

@dataclass
class ContextCheckValue:
    value: str

@dataclass
class ContextCheckPattern:
    value: str

ContextCheck = Union[ContextCheckValue, ContextCheckPattern]

@dataclass
class TypeRenamed:
    tpe: TypeId
    name: str

RuntimeId = int
MaterializerId = int
@dataclass
class TypeFunc:
    inp: TypeId
    out: TypeId
    mat: MaterializerId
    rate_calls: bool
    rate_weight: Optional[int]

@dataclass
class Policy:
    name: str
    materializer: MaterializerId

@dataclass
class FuncParams:
    inp: TypeId
    out: TypeId
    mat: MaterializerId

class Core:
    component: 'Root'
    
    def __init__(self, component: 'Root') -> None:
        self.component = component
    def init_typegraph(self, caller: wasmtime.Store, params: TypegraphInitParams) -> Result[None, Error]:
        ptr = self.component._realloc0(caller, 0, 0, 4, 116)
        assert(isinstance(ptr, int))
        record = params
        field = record.name
        field0 = record.dynamic
        field1 = record.path
        field2 = record.prefix
        field3 = record.cors
        field4 = record.auths
        field5 = record.rate
        ptr6, len7 = _encode_utf8(field, self.component._realloc0, self.component._core_memory0, caller)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 4, len7)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 0, ptr6)
        if field0 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, 0)
        else:
            payload8 = field0
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, 1)
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 9, int(payload8))
        ptr9, len10 = _encode_utf8(field1, self.component._realloc0, self.component._core_memory0, caller)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 16, len10)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 12, ptr9)
        if field2 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 20, 0)
        else:
            payload12 = field2
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 20, 1)
            ptr13, len14 = _encode_utf8(payload12, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 28, len14)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 24, ptr13)
        record15 = field3
        field16 = record15.allow_origin
        field17 = record15.allow_headers
        field18 = record15.expose_headers
        field19 = record15.allow_methods
        field20 = record15.allow_credentials
        field21 = record15.max_age_sec
        vec = field16
        len25 = len(vec)
        result = self.component._realloc0(caller, 0, 0, 4, len25 * 8)
        assert(isinstance(result, int))
        for i26 in range(0, len25):
            e = vec[i26]
            base22 = result + i26 * 8
            ptr23, len24 = _encode_utf8(e, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base22, 4, len24)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base22, 0, ptr23)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 36, len25)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 32, result)
        vec31 = field17
        len33 = len(vec31)
        result32 = self.component._realloc0(caller, 0, 0, 4, len33 * 8)
        assert(isinstance(result32, int))
        for i34 in range(0, len33):
            e27 = vec31[i34]
            base28 = result32 + i34 * 8
            ptr29, len30 = _encode_utf8(e27, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 4, len30)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 0, ptr29)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 44, len33)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 40, result32)
        vec39 = field18
        len41 = len(vec39)
        result40 = self.component._realloc0(caller, 0, 0, 4, len41 * 8)
        assert(isinstance(result40, int))
        for i42 in range(0, len41):
            e35 = vec39[i42]
            base36 = result40 + i42 * 8
            ptr37, len38 = _encode_utf8(e35, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base36, 4, len38)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base36, 0, ptr37)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 52, len41)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 48, result40)
        vec47 = field19
        len49 = len(vec47)
        result48 = self.component._realloc0(caller, 0, 0, 4, len49 * 8)
        assert(isinstance(result48, int))
        for i50 in range(0, len49):
            e43 = vec47[i50]
            base44 = result48 + i50 * 8
            ptr45, len46 = _encode_utf8(e43, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base44, 4, len46)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base44, 0, ptr45)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 60, len49)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 56, result48)
        _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, int(field20))
        if field21 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 68, 0)
        else:
            payload52 = field21
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 68, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 72, _clamp(payload52, 0, 4294967295))
        vec75 = field4
        len77 = len(vec75)
        result76 = self.component._realloc0(caller, 0, 0, 4, len77 * 20)
        assert(isinstance(result76, int))
        for i78 in range(0, len77):
            e53 = vec75[i78]
            base54 = result76 + i78 * 20
            record55 = e53
            field56 = record55.name
            field57 = record55.protocol
            field58 = record55.auth_data
            ptr59, len60 = _encode_utf8(field56, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base54, 4, len60)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base54, 0, ptr59)
            if isinstance(field57, AuthProtocolOauth2):
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base54, 8, 0)
            elif isinstance(field57, AuthProtocolJwt):
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base54, 8, 1)
            elif isinstance(field57, AuthProtocolBasic):
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base54, 8, 2)
            else:
                raise TypeError("invalid variant specified for AuthProtocol")
            vec71 = field58
            len73 = len(vec71)
            result72 = self.component._realloc0(caller, 0, 0, 4, len73 * 16)
            assert(isinstance(result72, int))
            for i74 in range(0, len73):
                e64 = vec71[i74]
                base65 = result72 + i74 * 16
                (tuplei,tuplei66,) = e64
                ptr67, len68 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base65, 4, len68)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base65, 0, ptr67)
                ptr69, len70 = _encode_utf8(tuplei66, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base65, 12, len70)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base65, 8, ptr69)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base54, 16, len73)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base54, 12, result72)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 80, len77)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 76, result76)
        if field5 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 84, 0)
        else:
            payload80 = field5
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 84, 1)
            record81 = payload80
            field82 = record81.window_limit
            field83 = record81.window_sec
            field84 = record81.query_limit
            field85 = record81.context_identifier
            field86 = record81.local_excess
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 88, _clamp(field82, 0, 4294967295))
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 92, _clamp(field83, 0, 4294967295))
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 96, _clamp(field84, 0, 4294967295))
            if field85 is None:
                _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 100, 0)
            else:
                payload88 = field85
                _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 100, 1)
                ptr89, len90 = _encode_utf8(payload88, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 108, len90)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 104, ptr89)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 112, _clamp(field86, 0, 4294967295))
        ret = self.component.lift_callee0(caller, ptr)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[None, Error]
        if load == 0:
            expected = Ok(None)
        elif load == 1:
            load91 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load92 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr98 = load91
            len99 = load92
            result100: List[str] = []
            for i101 in range(0, len99):
                base93 = ptr98 + i101 * 8
                load94 = _load(ctypes.c_int32, self.component._core_memory0, caller, base93, 0)
                load95 = _load(ctypes.c_int32, self.component._core_memory0, caller, base93, 4)
                ptr96 = load94
                len97 = load95
                list = _decode_utf8(self.component._core_memory0, caller, ptr96, len97)
                result100.append(list)
            expected = Err(Error(result100))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def finalize_typegraph(self, caller: wasmtime.Store) -> Result[str, Error]:
        ret = self.component.lift_callee1(caller)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[str, Error]
        if load == 0:
            load0 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load1 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr = load0
            len2 = load1
            list = _decode_utf8(self.component._core_memory0, caller, ptr, len2)
            expected = Ok(list)
        elif load == 1:
            load3 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load4 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr11 = load3
            len12 = load4
            result: List[str] = []
            for i13 in range(0, len12):
                base5 = ptr11 + i13 * 8
                load6 = _load(ctypes.c_int32, self.component._core_memory0, caller, base5, 0)
                load7 = _load(ctypes.c_int32, self.component._core_memory0, caller, base5, 4)
                ptr8 = load6
                len9 = load7
                list10 = _decode_utf8(self.component._core_memory0, caller, ptr8, len9)
                result.append(list10)
            expected = Err(Error(result))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return1(caller, ret)
        return expected
    def with_injection(self, caller: wasmtime.Store, data: TypeWithInjection) -> Result[TypeId, Error]:
        record = data
        field = record.tpe
        field0 = record.injection
        ptr, len1 = _encode_utf8(field0, self.component._realloc0, self.component._core_memory0, caller)
        ret = self.component.lift_callee2(caller, _clamp(field, 0, 4294967295), ptr, len1)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load2 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load2 & 0xffffffff)
        elif load == 1:
            load3 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load4 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr10 = load3
            len11 = load4
            result: List[str] = []
            for i12 in range(0, len11):
                base5 = ptr10 + i12 * 8
                load6 = _load(ctypes.c_int32, self.component._core_memory0, caller, base5, 0)
                load7 = _load(ctypes.c_int32, self.component._core_memory0, caller, base5, 4)
                ptr8 = load6
                len9 = load7
                list = _decode_utf8(self.component._core_memory0, caller, ptr8, len9)
                result.append(list)
            expected = Err(Error(result))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def proxyb(self, caller: wasmtime.Store, data: TypeProxy) -> Result[TypeId, Error]:
        record = data
        field = record.name
        field0 = record.extras
        ptr, len1 = _encode_utf8(field, self.component._realloc0, self.component._core_memory0, caller)
        vec = field0
        len8 = len(vec)
        result = self.component._realloc0(caller, 0, 0, 4, len8 * 16)
        assert(isinstance(result, int))
        for i9 in range(0, len8):
            e = vec[i9]
            base2 = result + i9 * 16
            (tuplei,tuplei3,) = e
            ptr4, len5 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base2, 4, len5)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base2, 0, ptr4)
            ptr6, len7 = _encode_utf8(tuplei3, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base2, 12, len7)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base2, 8, ptr6)
        ret = self.component.lift_callee3(caller, ptr, len1, result, len8)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load10 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load10 & 0xffffffff)
        elif load == 1:
            load11 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load12 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr18 = load11
            len19 = load12
            result20: List[str] = []
            for i21 in range(0, len19):
                base13 = ptr18 + i21 * 8
                load14 = _load(ctypes.c_int32, self.component._core_memory0, caller, base13, 0)
                load15 = _load(ctypes.c_int32, self.component._core_memory0, caller, base13, 4)
                ptr16 = load14
                len17 = load15
                list = _decode_utf8(self.component._core_memory0, caller, ptr16, len17)
                result20.append(list)
            expected = Err(Error(result20))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def integerb(self, caller: wasmtime.Store, data: TypeInteger, base: TypeBase) -> Result[TypeId, Error]:
        ptr = self.component._realloc0(caller, 0, 0, 4, 80)
        assert(isinstance(ptr, int))
        record = data
        field = record.min
        field0 = record.max
        field1 = record.exclusive_minimum
        field2 = record.exclusive_maximum
        field3 = record.multiple_of
        field4 = record.enumeration
        if field is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 0, 0)
        else:
            payload5 = field
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 0, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 4, _clamp(payload5, -2147483648, 2147483647))
        if field0 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, 0)
        else:
            payload7 = field0
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 12, _clamp(payload7, -2147483648, 2147483647))
        if field1 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 16, 0)
        else:
            payload9 = field1
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 16, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 20, _clamp(payload9, -2147483648, 2147483647))
        if field2 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 24, 0)
        else:
            payload11 = field2
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 24, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 28, _clamp(payload11, -2147483648, 2147483647))
        if field3 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 32, 0)
        else:
            payload13 = field3
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 32, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 36, _clamp(payload13, -2147483648, 2147483647))
        if field4 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 40, 0)
        else:
            payload15 = field4
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 40, 1)
            ptr16, len17 = _list_canon_lower(payload15, ctypes.c_int32, 4, 4, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 48, len17)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 44, ptr16)
        record18 = base
        field19 = record18.name
        field20 = record18.runtime_config
        field21 = record18.as_id
        if field19 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 52, 0)
        else:
            payload23 = field19
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 52, 1)
            ptr24, len25 = _encode_utf8(payload23, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 60, len25)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 56, ptr24)
        if field20 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, 0)
        else:
            payload27 = field20
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, 1)
            vec = payload27
            len34 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len34 * 16)
            assert(isinstance(result, int))
            for i35 in range(0, len34):
                e = vec[i35]
                base28 = result + i35 * 16
                (tuplei,tuplei29,) = e
                ptr30, len31 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 4, len31)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 0, ptr30)
                ptr32, len33 = _encode_utf8(tuplei29, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 12, len33)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 8, ptr32)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 72, len34)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 68, result)
        _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 76, int(field21))
        ret = self.component.lift_callee4(caller, ptr)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load36 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load36 & 0xffffffff)
        elif load == 1:
            load37 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load38 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr44 = load37
            len45 = load38
            result46: List[str] = []
            for i47 in range(0, len45):
                base39 = ptr44 + i47 * 8
                load40 = _load(ctypes.c_int32, self.component._core_memory0, caller, base39, 0)
                load41 = _load(ctypes.c_int32, self.component._core_memory0, caller, base39, 4)
                ptr42 = load40
                len43 = load41
                list = _decode_utf8(self.component._core_memory0, caller, ptr42, len43)
                result46.append(list)
            expected = Err(Error(result46))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def floatb(self, caller: wasmtime.Store, data: TypeFloat, base: TypeBase) -> Result[TypeId, Error]:
        ptr = self.component._realloc0(caller, 0, 0, 8, 128)
        assert(isinstance(ptr, int))
        record = data
        field = record.min
        field0 = record.max
        field1 = record.exclusive_minimum
        field2 = record.exclusive_maximum
        field3 = record.multiple_of
        field4 = record.enumeration
        if field is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 0, 0)
        else:
            payload5 = field
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 0, 1)
            _store(ctypes.c_double, self.component._core_memory0, caller, ptr, 8, payload5)
        if field0 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 16, 0)
        else:
            payload7 = field0
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 16, 1)
            _store(ctypes.c_double, self.component._core_memory0, caller, ptr, 24, payload7)
        if field1 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 32, 0)
        else:
            payload9 = field1
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 32, 1)
            _store(ctypes.c_double, self.component._core_memory0, caller, ptr, 40, payload9)
        if field2 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 48, 0)
        else:
            payload11 = field2
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 48, 1)
            _store(ctypes.c_double, self.component._core_memory0, caller, ptr, 56, payload11)
        if field3 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, 0)
        else:
            payload13 = field3
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, 1)
            _store(ctypes.c_double, self.component._core_memory0, caller, ptr, 72, payload13)
        if field4 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 80, 0)
        else:
            payload15 = field4
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 80, 1)
            ptr16, len17 = _list_canon_lower(payload15, ctypes.c_double, 8, 8, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 88, len17)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 84, ptr16)
        record18 = base
        field19 = record18.name
        field20 = record18.runtime_config
        field21 = record18.as_id
        if field19 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 96, 0)
        else:
            payload23 = field19
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 96, 1)
            ptr24, len25 = _encode_utf8(payload23, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 104, len25)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 100, ptr24)
        if field20 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 108, 0)
        else:
            payload27 = field20
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 108, 1)
            vec = payload27
            len34 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len34 * 16)
            assert(isinstance(result, int))
            for i35 in range(0, len34):
                e = vec[i35]
                base28 = result + i35 * 16
                (tuplei,tuplei29,) = e
                ptr30, len31 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 4, len31)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 0, ptr30)
                ptr32, len33 = _encode_utf8(tuplei29, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 12, len33)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base28, 8, ptr32)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 116, len34)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 112, result)
        _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 120, int(field21))
        ret = self.component.lift_callee5(caller, ptr)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load36 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load36 & 0xffffffff)
        elif load == 1:
            load37 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load38 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr44 = load37
            len45 = load38
            result46: List[str] = []
            for i47 in range(0, len45):
                base39 = ptr44 + i47 * 8
                load40 = _load(ctypes.c_int32, self.component._core_memory0, caller, base39, 0)
                load41 = _load(ctypes.c_int32, self.component._core_memory0, caller, base39, 4)
                ptr42 = load40
                len43 = load41
                list = _decode_utf8(self.component._core_memory0, caller, ptr42, len43)
                result46.append(list)
            expected = Err(Error(result46))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def booleanb(self, caller: wasmtime.Store, base: TypeBase) -> Result[TypeId, Error]:
        record = base
        field = record.name
        field0 = record.runtime_config
        field1 = record.as_id
        if field is None:
            variant = 0
            variant4 = 0
            variant5 = 0
        else:
            payload2 = field
            ptr, len3 = _encode_utf8(payload2, self.component._realloc0, self.component._core_memory0, caller)
            variant = 1
            variant4 = ptr
            variant5 = len3
        if field0 is None:
            variant16 = 0
            variant17 = 0
            variant18 = 0
        else:
            payload7 = field0
            vec = payload7
            len14 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len14 * 16)
            assert(isinstance(result, int))
            for i15 in range(0, len14):
                e = vec[i15]
                base8 = result + i15 * 16
                (tuplei,tuplei9,) = e
                ptr10, len11 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base8, 4, len11)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base8, 0, ptr10)
                ptr12, len13 = _encode_utf8(tuplei9, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base8, 12, len13)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base8, 8, ptr12)
            variant16 = 1
            variant17 = result
            variant18 = len14
        ret = self.component.lift_callee6(caller, variant, variant4, variant5, variant16, variant17, variant18, int(field1))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load19 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load19 & 0xffffffff)
        elif load == 1:
            load20 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load21 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr27 = load20
            len28 = load21
            result29: List[str] = []
            for i30 in range(0, len28):
                base22 = ptr27 + i30 * 8
                load23 = _load(ctypes.c_int32, self.component._core_memory0, caller, base22, 0)
                load24 = _load(ctypes.c_int32, self.component._core_memory0, caller, base22, 4)
                ptr25 = load23
                len26 = load24
                list = _decode_utf8(self.component._core_memory0, caller, ptr25, len26)
                result29.append(list)
            expected = Err(Error(result29))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def stringb(self, caller: wasmtime.Store, data: TypeString, base: TypeBase) -> Result[TypeId, Error]:
        ptr = self.component._realloc0(caller, 0, 0, 4, 80)
        assert(isinstance(ptr, int))
        record = data
        field = record.min
        field0 = record.max
        field1 = record.format
        field2 = record.pattern
        field3 = record.enumeration
        if field is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 0, 0)
        else:
            payload4 = field
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 0, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 4, _clamp(payload4, 0, 4294967295))
        if field0 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, 0)
        else:
            payload6 = field0
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 12, _clamp(payload6, 0, 4294967295))
        if field1 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 16, 0)
        else:
            payload8 = field1
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 16, 1)
            ptr9, len10 = _encode_utf8(payload8, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 24, len10)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 20, ptr9)
        if field2 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 28, 0)
        else:
            payload12 = field2
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 28, 1)
            ptr13, len14 = _encode_utf8(payload12, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 36, len14)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 32, ptr13)
        if field3 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 40, 0)
        else:
            payload16 = field3
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 40, 1)
            vec = payload16
            len20 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len20 * 8)
            assert(isinstance(result, int))
            for i21 in range(0, len20):
                e = vec[i21]
                base17 = result + i21 * 8
                ptr18, len19 = _encode_utf8(e, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base17, 4, len19)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base17, 0, ptr18)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 48, len20)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 44, result)
        record22 = base
        field23 = record22.name
        field24 = record22.runtime_config
        field25 = record22.as_id
        if field23 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 52, 0)
        else:
            payload27 = field23
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 52, 1)
            ptr28, len29 = _encode_utf8(payload27, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 60, len29)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 56, ptr28)
        if field24 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, 0)
        else:
            payload31 = field24
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, 1)
            vec39 = payload31
            len41 = len(vec39)
            result40 = self.component._realloc0(caller, 0, 0, 4, len41 * 16)
            assert(isinstance(result40, int))
            for i42 in range(0, len41):
                e32 = vec39[i42]
                base33 = result40 + i42 * 16
                (tuplei,tuplei34,) = e32
                ptr35, len36 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base33, 4, len36)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base33, 0, ptr35)
                ptr37, len38 = _encode_utf8(tuplei34, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base33, 12, len38)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base33, 8, ptr37)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 72, len41)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 68, result40)
        _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 76, int(field25))
        ret = self.component.lift_callee7(caller, ptr)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load43 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load43 & 0xffffffff)
        elif load == 1:
            load44 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load45 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr51 = load44
            len52 = load45
            result53: List[str] = []
            for i54 in range(0, len52):
                base46 = ptr51 + i54 * 8
                load47 = _load(ctypes.c_int32, self.component._core_memory0, caller, base46, 0)
                load48 = _load(ctypes.c_int32, self.component._core_memory0, caller, base46, 4)
                ptr49 = load47
                len50 = load48
                list = _decode_utf8(self.component._core_memory0, caller, ptr49, len50)
                result53.append(list)
            expected = Err(Error(result53))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def fileb(self, caller: wasmtime.Store, data: TypeFile, base: TypeBase) -> Result[TypeId, Error]:
        record = data
        field = record.min
        field0 = record.max
        field1 = record.allow
        if field is None:
            variant = 0
            variant3 = 0
        else:
            payload2 = field
            variant = 1
            variant3 = _clamp(payload2, 0, 4294967295)
        if field0 is None:
            variant6 = 0
            variant7 = 0
        else:
            payload5 = field0
            variant6 = 1
            variant7 = _clamp(payload5, 0, 4294967295)
        if field1 is None:
            variant14 = 0
            variant15 = 0
            variant16 = 0
        else:
            payload9 = field1
            vec = payload9
            len12 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len12 * 8)
            assert(isinstance(result, int))
            for i13 in range(0, len12):
                e = vec[i13]
                base10 = result + i13 * 8
                ptr, len11 = _encode_utf8(e, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 4, len11)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 0, ptr)
            variant14 = 1
            variant15 = result
            variant16 = len12
        record17 = base
        field18 = record17.name
        field19 = record17.runtime_config
        field20 = record17.as_id
        if field18 is None:
            variant25 = 0
            variant26 = 0
            variant27 = 0
        else:
            payload22 = field18
            ptr23, len24 = _encode_utf8(payload22, self.component._realloc0, self.component._core_memory0, caller)
            variant25 = 1
            variant26 = ptr23
            variant27 = len24
        if field19 is None:
            variant41 = 0
            variant42 = 0
            variant43 = 0
        else:
            payload29 = field19
            vec37 = payload29
            len39 = len(vec37)
            result38 = self.component._realloc0(caller, 0, 0, 4, len39 * 16)
            assert(isinstance(result38, int))
            for i40 in range(0, len39):
                e30 = vec37[i40]
                base31 = result38 + i40 * 16
                (tuplei,tuplei32,) = e30
                ptr33, len34 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base31, 4, len34)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base31, 0, ptr33)
                ptr35, len36 = _encode_utf8(tuplei32, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base31, 12, len36)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base31, 8, ptr35)
            variant41 = 1
            variant42 = result38
            variant43 = len39
        ret = self.component.lift_callee8(caller, variant, variant3, variant6, variant7, variant14, variant15, variant16, variant25, variant26, variant27, variant41, variant42, variant43, int(field20))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load44 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load44 & 0xffffffff)
        elif load == 1:
            load45 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load46 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr52 = load45
            len53 = load46
            result54: List[str] = []
            for i55 in range(0, len53):
                base47 = ptr52 + i55 * 8
                load48 = _load(ctypes.c_int32, self.component._core_memory0, caller, base47, 0)
                load49 = _load(ctypes.c_int32, self.component._core_memory0, caller, base47, 4)
                ptr50 = load48
                len51 = load49
                list = _decode_utf8(self.component._core_memory0, caller, ptr50, len51)
                result54.append(list)
            expected = Err(Error(result54))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def arrayb(self, caller: wasmtime.Store, data: TypeArray, base: TypeBase) -> Result[TypeId, Error]:
        record = data
        field = record.of
        field0 = record.min
        field1 = record.max
        field2 = record.unique_items
        if field0 is None:
            variant = 0
            variant4 = 0
        else:
            payload3 = field0
            variant = 1
            variant4 = _clamp(payload3, 0, 4294967295)
        if field1 is None:
            variant7 = 0
            variant8 = 0
        else:
            payload6 = field1
            variant7 = 1
            variant8 = _clamp(payload6, 0, 4294967295)
        if field2 is None:
            variant11 = 0
            variant12 = 0
        else:
            payload10 = field2
            variant11 = 1
            variant12 = int(payload10)
        record13 = base
        field14 = record13.name
        field15 = record13.runtime_config
        field16 = record13.as_id
        if field14 is None:
            variant20 = 0
            variant21 = 0
            variant22 = 0
        else:
            payload18 = field14
            ptr, len19 = _encode_utf8(payload18, self.component._realloc0, self.component._core_memory0, caller)
            variant20 = 1
            variant21 = ptr
            variant22 = len19
        if field15 is None:
            variant33 = 0
            variant34 = 0
            variant35 = 0
        else:
            payload24 = field15
            vec = payload24
            len31 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len31 * 16)
            assert(isinstance(result, int))
            for i32 in range(0, len31):
                e = vec[i32]
                base25 = result + i32 * 16
                (tuplei,tuplei26,) = e
                ptr27, len28 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base25, 4, len28)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base25, 0, ptr27)
                ptr29, len30 = _encode_utf8(tuplei26, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base25, 12, len30)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base25, 8, ptr29)
            variant33 = 1
            variant34 = result
            variant35 = len31
        ret = self.component.lift_callee9(caller, _clamp(field, 0, 4294967295), variant, variant4, variant7, variant8, variant11, variant12, variant20, variant21, variant22, variant33, variant34, variant35, int(field16))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load36 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load36 & 0xffffffff)
        elif load == 1:
            load37 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load38 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr44 = load37
            len45 = load38
            result46: List[str] = []
            for i47 in range(0, len45):
                base39 = ptr44 + i47 * 8
                load40 = _load(ctypes.c_int32, self.component._core_memory0, caller, base39, 0)
                load41 = _load(ctypes.c_int32, self.component._core_memory0, caller, base39, 4)
                ptr42 = load40
                len43 = load41
                list = _decode_utf8(self.component._core_memory0, caller, ptr42, len43)
                result46.append(list)
            expected = Err(Error(result46))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def optionalb(self, caller: wasmtime.Store, data: TypeOptional, base: TypeBase) -> Result[TypeId, Error]:
        record = data
        field = record.of
        field0 = record.default_item
        if field0 is None:
            variant = 0
            variant3 = 0
            variant4 = 0
        else:
            payload1 = field0
            ptr, len2 = _encode_utf8(payload1, self.component._realloc0, self.component._core_memory0, caller)
            variant = 1
            variant3 = ptr
            variant4 = len2
        record5 = base
        field6 = record5.name
        field7 = record5.runtime_config
        field8 = record5.as_id
        if field6 is None:
            variant13 = 0
            variant14 = 0
            variant15 = 0
        else:
            payload10 = field6
            ptr11, len12 = _encode_utf8(payload10, self.component._realloc0, self.component._core_memory0, caller)
            variant13 = 1
            variant14 = ptr11
            variant15 = len12
        if field7 is None:
            variant26 = 0
            variant27 = 0
            variant28 = 0
        else:
            payload17 = field7
            vec = payload17
            len24 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len24 * 16)
            assert(isinstance(result, int))
            for i25 in range(0, len24):
                e = vec[i25]
                base18 = result + i25 * 16
                (tuplei,tuplei19,) = e
                ptr20, len21 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base18, 4, len21)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base18, 0, ptr20)
                ptr22, len23 = _encode_utf8(tuplei19, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base18, 12, len23)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base18, 8, ptr22)
            variant26 = 1
            variant27 = result
            variant28 = len24
        ret = self.component.lift_callee10(caller, _clamp(field, 0, 4294967295), variant, variant3, variant4, variant13, variant14, variant15, variant26, variant27, variant28, int(field8))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load29 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load29 & 0xffffffff)
        elif load == 1:
            load30 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load31 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr37 = load30
            len38 = load31
            result39: List[str] = []
            for i40 in range(0, len38):
                base32 = ptr37 + i40 * 8
                load33 = _load(ctypes.c_int32, self.component._core_memory0, caller, base32, 0)
                load34 = _load(ctypes.c_int32, self.component._core_memory0, caller, base32, 4)
                ptr35 = load33
                len36 = load34
                list = _decode_utf8(self.component._core_memory0, caller, ptr35, len36)
                result39.append(list)
            expected = Err(Error(result39))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def unionb(self, caller: wasmtime.Store, data: TypeUnion, base: TypeBase) -> Result[TypeId, Error]:
        record = data
        field = record.variants
        ptr, len0 = _list_canon_lower(field, ctypes.c_uint32, 4, 4, self.component._realloc0, self.component._core_memory0, caller)
        record1 = base
        field2 = record1.name
        field3 = record1.runtime_config
        field4 = record1.as_id
        if field2 is None:
            variant = 0
            variant8 = 0
            variant9 = 0
        else:
            payload5 = field2
            ptr6, len7 = _encode_utf8(payload5, self.component._realloc0, self.component._core_memory0, caller)
            variant = 1
            variant8 = ptr6
            variant9 = len7
        if field3 is None:
            variant20 = 0
            variant21 = 0
            variant22 = 0
        else:
            payload11 = field3
            vec = payload11
            len18 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len18 * 16)
            assert(isinstance(result, int))
            for i19 in range(0, len18):
                e = vec[i19]
                base12 = result + i19 * 16
                (tuplei,tuplei13,) = e
                ptr14, len15 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 4, len15)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 0, ptr14)
                ptr16, len17 = _encode_utf8(tuplei13, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 12, len17)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 8, ptr16)
            variant20 = 1
            variant21 = result
            variant22 = len18
        ret = self.component.lift_callee11(caller, ptr, len0, variant, variant8, variant9, variant20, variant21, variant22, int(field4))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load23 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load23 & 0xffffffff)
        elif load == 1:
            load24 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load25 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr31 = load24
            len32 = load25
            result33: List[str] = []
            for i34 in range(0, len32):
                base26 = ptr31 + i34 * 8
                load27 = _load(ctypes.c_int32, self.component._core_memory0, caller, base26, 0)
                load28 = _load(ctypes.c_int32, self.component._core_memory0, caller, base26, 4)
                ptr29 = load27
                len30 = load28
                list = _decode_utf8(self.component._core_memory0, caller, ptr29, len30)
                result33.append(list)
            expected = Err(Error(result33))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def eitherb(self, caller: wasmtime.Store, data: TypeEither, base: TypeBase) -> Result[TypeId, Error]:
        record = data
        field = record.variants
        ptr, len0 = _list_canon_lower(field, ctypes.c_uint32, 4, 4, self.component._realloc0, self.component._core_memory0, caller)
        record1 = base
        field2 = record1.name
        field3 = record1.runtime_config
        field4 = record1.as_id
        if field2 is None:
            variant = 0
            variant8 = 0
            variant9 = 0
        else:
            payload5 = field2
            ptr6, len7 = _encode_utf8(payload5, self.component._realloc0, self.component._core_memory0, caller)
            variant = 1
            variant8 = ptr6
            variant9 = len7
        if field3 is None:
            variant20 = 0
            variant21 = 0
            variant22 = 0
        else:
            payload11 = field3
            vec = payload11
            len18 = len(vec)
            result = self.component._realloc0(caller, 0, 0, 4, len18 * 16)
            assert(isinstance(result, int))
            for i19 in range(0, len18):
                e = vec[i19]
                base12 = result + i19 * 16
                (tuplei,tuplei13,) = e
                ptr14, len15 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 4, len15)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 0, ptr14)
                ptr16, len17 = _encode_utf8(tuplei13, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 12, len17)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base12, 8, ptr16)
            variant20 = 1
            variant21 = result
            variant22 = len18
        ret = self.component.lift_callee12(caller, ptr, len0, variant, variant8, variant9, variant20, variant21, variant22, int(field4))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load23 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load23 & 0xffffffff)
        elif load == 1:
            load24 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load25 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr31 = load24
            len32 = load25
            result33: List[str] = []
            for i34 in range(0, len32):
                base26 = ptr31 + i34 * 8
                load27 = _load(ctypes.c_int32, self.component._core_memory0, caller, base26, 0)
                load28 = _load(ctypes.c_int32, self.component._core_memory0, caller, base26, 4)
                ptr29 = load27
                len30 = load28
                list = _decode_utf8(self.component._core_memory0, caller, ptr29, len30)
                result33.append(list)
            expected = Err(Error(result33))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def structb(self, caller: wasmtime.Store, data: TypeStruct, base: TypeBase) -> Result[TypeId, Error]:
        ptr = self.component._realloc0(caller, 0, 0, 4, 68)
        assert(isinstance(ptr, int))
        record = data
        field = record.props
        field0 = record.additional_props
        field1 = record.min
        field2 = record.max
        field3 = record.enumeration
        vec = field
        len8 = len(vec)
        result = self.component._realloc0(caller, 0, 0, 4, len8 * 12)
        assert(isinstance(result, int))
        for i9 in range(0, len8):
            e = vec[i9]
            base4 = result + i9 * 12
            (tuplei,tuplei5,) = e
            ptr6, len7 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base4, 4, len7)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base4, 0, ptr6)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base4, 8, _clamp(tuplei5, 0, 4294967295))
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 4, len8)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 0, result)
        _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 8, int(field0))
        if field1 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 12, 0)
        else:
            payload10 = field1
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 12, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 16, _clamp(payload10, 0, 4294967295))
        if field2 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 20, 0)
        else:
            payload12 = field2
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 20, 1)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 24, _clamp(payload12, 0, 4294967295))
        if field3 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 28, 0)
        else:
            payload14 = field3
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 28, 1)
            vec19 = payload14
            len21 = len(vec19)
            result20 = self.component._realloc0(caller, 0, 0, 4, len21 * 8)
            assert(isinstance(result20, int))
            for i22 in range(0, len21):
                e15 = vec19[i22]
                base16 = result20 + i22 * 8
                ptr17, len18 = _encode_utf8(e15, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base16, 4, len18)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base16, 0, ptr17)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 36, len21)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 32, result20)
        record23 = base
        field24 = record23.name
        field25 = record23.runtime_config
        field26 = record23.as_id
        if field24 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 40, 0)
        else:
            payload28 = field24
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 40, 1)
            ptr29, len30 = _encode_utf8(payload28, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 48, len30)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 44, ptr29)
        if field25 is None:
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 52, 0)
        else:
            payload32 = field25
            _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 52, 1)
            vec41 = payload32
            len43 = len(vec41)
            result42 = self.component._realloc0(caller, 0, 0, 4, len43 * 16)
            assert(isinstance(result42, int))
            for i44 in range(0, len43):
                e33 = vec41[i44]
                base34 = result42 + i44 * 16
                (tuplei35,tuplei36,) = e33
                ptr37, len38 = _encode_utf8(tuplei35, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base34, 4, len38)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base34, 0, ptr37)
                ptr39, len40 = _encode_utf8(tuplei36, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base34, 12, len40)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base34, 8, ptr39)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 60, len43)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 56, result42)
        _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 64, int(field26))
        ret = self.component.lift_callee13(caller, ptr)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load45 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load45 & 0xffffffff)
        elif load == 1:
            load46 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load47 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr53 = load46
            len54 = load47
            result55: List[str] = []
            for i56 in range(0, len54):
                base48 = ptr53 + i56 * 8
                load49 = _load(ctypes.c_int32, self.component._core_memory0, caller, base48, 0)
                load50 = _load(ctypes.c_int32, self.component._core_memory0, caller, base48, 4)
                ptr51 = load49
                len52 = load50
                list = _decode_utf8(self.component._core_memory0, caller, ptr51, len52)
                result55.append(list)
            expected = Err(Error(result55))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def get_type_repr(self, caller: wasmtime.Store, id: TypeId) -> Result[str, Error]:
        ret = self.component.lift_callee14(caller, _clamp(id, 0, 4294967295))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[str, Error]
        if load == 0:
            load0 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load1 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr = load0
            len2 = load1
            list = _decode_utf8(self.component._core_memory0, caller, ptr, len2)
            expected = Ok(list)
        elif load == 1:
            load3 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load4 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr11 = load3
            len12 = load4
            result: List[str] = []
            for i13 in range(0, len12):
                base5 = ptr11 + i13 * 8
                load6 = _load(ctypes.c_int32, self.component._core_memory0, caller, base5, 0)
                load7 = _load(ctypes.c_int32, self.component._core_memory0, caller, base5, 4)
                ptr8 = load6
                len9 = load7
                list10 = _decode_utf8(self.component._core_memory0, caller, ptr8, len9)
                result.append(list10)
            expected = Err(Error(result))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return1(caller, ret)
        return expected
    def funcb(self, caller: wasmtime.Store, data: TypeFunc) -> Result[TypeId, Error]:
        record = data
        field = record.inp
        field0 = record.out
        field1 = record.mat
        field2 = record.rate_calls
        field3 = record.rate_weight
        if field3 is None:
            variant = 0
            variant5 = 0
        else:
            payload4 = field3
            variant = 1
            variant5 = _clamp(payload4, 0, 4294967295)
        ret = self.component.lift_callee15(caller, _clamp(field, 0, 4294967295), _clamp(field0, 0, 4294967295), _clamp(field1, 0, 4294967295), int(field2), variant, variant5)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load6 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load6 & 0xffffffff)
        elif load == 1:
            load7 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load8 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr13 = load7
            len14 = load8
            result: List[str] = []
            for i15 in range(0, len14):
                base9 = ptr13 + i15 * 8
                load10 = _load(ctypes.c_int32, self.component._core_memory0, caller, base9, 0)
                load11 = _load(ctypes.c_int32, self.component._core_memory0, caller, base9, 4)
                ptr = load10
                len12 = load11
                list = _decode_utf8(self.component._core_memory0, caller, ptr, len12)
                result.append(list)
            expected = Err(Error(result))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def register_policy(self, caller: wasmtime.Store, pol: Policy) -> Result[PolicyId, Error]:
        record = pol
        field = record.name
        field0 = record.materializer
        ptr, len1 = _encode_utf8(field, self.component._realloc0, self.component._core_memory0, caller)
        ret = self.component.lift_callee16(caller, ptr, len1, _clamp(field0, 0, 4294967295))
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[PolicyId, Error]
        if load == 0:
            load2 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load2 & 0xffffffff)
        elif load == 1:
            load3 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load4 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr10 = load3
            len11 = load4
            result: List[str] = []
            for i12 in range(0, len11):
                base5 = ptr10 + i12 * 8
                load6 = _load(ctypes.c_int32, self.component._core_memory0, caller, base5, 0)
                load7 = _load(ctypes.c_int32, self.component._core_memory0, caller, base5, 4)
                ptr8 = load6
                len9 = load7
                list = _decode_utf8(self.component._core_memory0, caller, ptr8, len9)
                result.append(list)
            expected = Err(Error(result))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def with_policy(self, caller: wasmtime.Store, data: TypePolicy) -> Result[TypeId, Error]:
        record = data
        field = record.tpe
        field0 = record.chain
        vec = field0
        len16 = len(vec)
        result = self.component._realloc0(caller, 0, 0, 4, len16 * 36)
        assert(isinstance(result, int))
        for i17 in range(0, len16):
            e = vec[i17]
            base1 = result + i17 * 36
            if isinstance(e, PolicySpecSimple):
                payload = e.value
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 0, 0)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base1, 4, _clamp(payload, 0, 4294967295))
            elif isinstance(e, PolicySpecPerEffect):
                payload2 = e.value
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 0, 1)
                record3 = payload2
                field4 = record3.read
                field5 = record3.create
                field6 = record3.update
                field7 = record3.delete
                if field4 is None:
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 4, 0)
                else:
                    payload9 = field4
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 4, 1)
                    _store(ctypes.c_uint32, self.component._core_memory0, caller, base1, 8, _clamp(payload9, 0, 4294967295))
                if field5 is None:
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 12, 0)
                else:
                    payload11 = field5
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 12, 1)
                    _store(ctypes.c_uint32, self.component._core_memory0, caller, base1, 16, _clamp(payload11, 0, 4294967295))
                if field6 is None:
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 20, 0)
                else:
                    payload13 = field6
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 20, 1)
                    _store(ctypes.c_uint32, self.component._core_memory0, caller, base1, 24, _clamp(payload13, 0, 4294967295))
                if field7 is None:
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 28, 0)
                else:
                    payload15 = field7
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base1, 28, 1)
                    _store(ctypes.c_uint32, self.component._core_memory0, caller, base1, 32, _clamp(payload15, 0, 4294967295))
            else:
                raise TypeError("invalid variant specified for PolicySpec")
        ret = self.component.lift_callee17(caller, _clamp(field, 0, 4294967295), result, len16)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load18 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load18 & 0xffffffff)
        elif load == 1:
            load19 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load20 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr25 = load19
            len26 = load20
            result27: List[str] = []
            for i28 in range(0, len26):
                base21 = ptr25 + i28 * 8
                load22 = _load(ctypes.c_int32, self.component._core_memory0, caller, base21, 0)
                load23 = _load(ctypes.c_int32, self.component._core_memory0, caller, base21, 4)
                ptr = load22
                len24 = load23
                list = _decode_utf8(self.component._core_memory0, caller, ptr, len24)
                result27.append(list)
            expected = Err(Error(result27))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def register_context_policy(self, caller: wasmtime.Store, key: str, check: ContextCheck) -> Result[Tuple[PolicyId, str], Error]:
        ptr, len0 = _encode_utf8(key, self.component._realloc0, self.component._core_memory0, caller)
        if isinstance(check, ContextCheckValue):
            payload = check.value
            ptr1, len2 = _encode_utf8(payload, self.component._realloc0, self.component._core_memory0, caller)
            variant = 0
            variant6 = ptr1
            variant7 = len2
        elif isinstance(check, ContextCheckPattern):
            payload3 = check.value
            ptr4, len5 = _encode_utf8(payload3, self.component._realloc0, self.component._core_memory0, caller)
            variant = 1
            variant6 = ptr4
            variant7 = len5
        else:
            raise TypeError("invalid variant specified for ContextCheck")
        ret = self.component.lift_callee18(caller, ptr, len0, variant, variant6, variant7)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[Tuple[PolicyId, str], Error]
        if load == 0:
            load8 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load9 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            load10 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 12)
            ptr11 = load9
            len12 = load10
            list = _decode_utf8(self.component._core_memory0, caller, ptr11, len12)
            expected = Ok((load8 & 0xffffffff, list,))
        elif load == 1:
            load13 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load14 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr21 = load13
            len22 = load14
            result: List[str] = []
            for i23 in range(0, len22):
                base15 = ptr21 + i23 * 8
                load16 = _load(ctypes.c_int32, self.component._core_memory0, caller, base15, 0)
                load17 = _load(ctypes.c_int32, self.component._core_memory0, caller, base15, 4)
                ptr18 = load16
                len19 = load17
                list20 = _decode_utf8(self.component._core_memory0, caller, ptr18, len19)
                result.append(list20)
            expected = Err(Error(result))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return2(caller, ret)
        return expected
    def rename_type(self, caller: wasmtime.Store, tpe: TypeId, new_name: str) -> Result[TypeId, Error]:
        ptr, len0 = _encode_utf8(new_name, self.component._realloc0, self.component._core_memory0, caller)
        ret = self.component.lift_callee19(caller, _clamp(tpe, 0, 4294967295), ptr, len0)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[TypeId, Error]
        if load == 0:
            load1 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            expected = Ok(load1 & 0xffffffff)
        elif load == 1:
            load2 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load3 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr9 = load2
            len10 = load3
            result: List[str] = []
            for i11 in range(0, len10):
                base4 = ptr9 + i11 * 8
                load5 = _load(ctypes.c_int32, self.component._core_memory0, caller, base4, 0)
                load6 = _load(ctypes.c_int32, self.component._core_memory0, caller, base4, 4)
                ptr7 = load5
                len8 = load6
                list = _decode_utf8(self.component._core_memory0, caller, ptr7, len8)
                result.append(list)
            expected = Err(Error(result))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
    def expose(self, caller: wasmtime.Store, fns: List[Tuple[str, TypeId]], default_policy: Optional[List[PolicySpec]]) -> Result[None, Error]:
        vec = fns
        len3 = len(vec)
        result = self.component._realloc0(caller, 0, 0, 4, len3 * 12)
        assert(isinstance(result, int))
        for i4 in range(0, len3):
            e = vec[i4]
            base0 = result + i4 * 12
            (tuplei,tuplei1,) = e
            ptr, len2 = _encode_utf8(tuplei, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base0, 4, len2)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base0, 0, ptr)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base0, 8, _clamp(tuplei1, 0, 4294967295))
        if default_policy is None:
            variant = 0
            variant25 = 0
            variant26 = 0
        else:
            payload5 = default_policy
            vec21 = payload5
            len23 = len(vec21)
            result22 = self.component._realloc0(caller, 0, 0, 4, len23 * 36)
            assert(isinstance(result22, int))
            for i24 in range(0, len23):
                e6 = vec21[i24]
                base7 = result22 + i24 * 36
                if isinstance(e6, PolicySpecSimple):
                    payload8 = e6.value
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 0, 0)
                    _store(ctypes.c_uint32, self.component._core_memory0, caller, base7, 4, _clamp(payload8, 0, 4294967295))
                elif isinstance(e6, PolicySpecPerEffect):
                    payload9 = e6.value
                    _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 0, 1)
                    record = payload9
                    field = record.read
                    field10 = record.create
                    field11 = record.update
                    field12 = record.delete
                    if field is None:
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 4, 0)
                    else:
                        payload14 = field
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 4, 1)
                        _store(ctypes.c_uint32, self.component._core_memory0, caller, base7, 8, _clamp(payload14, 0, 4294967295))
                    if field10 is None:
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 12, 0)
                    else:
                        payload16 = field10
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 12, 1)
                        _store(ctypes.c_uint32, self.component._core_memory0, caller, base7, 16, _clamp(payload16, 0, 4294967295))
                    if field11 is None:
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 20, 0)
                    else:
                        payload18 = field11
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 20, 1)
                        _store(ctypes.c_uint32, self.component._core_memory0, caller, base7, 24, _clamp(payload18, 0, 4294967295))
                    if field12 is None:
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 28, 0)
                    else:
                        payload20 = field12
                        _store(ctypes.c_uint8, self.component._core_memory0, caller, base7, 28, 1)
                        _store(ctypes.c_uint32, self.component._core_memory0, caller, base7, 32, _clamp(payload20, 0, 4294967295))
                else:
                    raise TypeError("invalid variant specified for PolicySpec")
            variant = 1
            variant25 = result22
            variant26 = len23
        ret = self.component.lift_callee20(caller, result, len3, variant, variant25, variant26)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[None, Error]
        if load == 0:
            expected = Ok(None)
        elif load == 1:
            load27 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load28 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr34 = load27
            len35 = load28
            result36: List[str] = []
            for i37 in range(0, len35):
                base29 = ptr34 + i37 * 8
                load30 = _load(ctypes.c_int32, self.component._core_memory0, caller, base29, 0)
                load31 = _load(ctypes.c_int32, self.component._core_memory0, caller, base29, 4)
                ptr32 = load30
                len33 = load31
                list = _decode_utf8(self.component._core_memory0, caller, ptr32, len33)
                result36.append(list)
            expected = Err(Error(result36))
        else:
            raise TypeError("invalid variant discriminant for expected")
        self.component._post_return0(caller, ret)
        return expected
