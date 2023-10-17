from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataMeta(_message.Message):
    __slots__ = ["data", "desc"]
    class DescEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    desc: _containers.ScalarMap[str, str]
    def __init__(self, data: _Optional[bytes] = ..., desc: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ReqData(_message.Message):
    __slots__ = ["data", "op", "param", "s"]
    class ParamEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    OP_FIELD_NUMBER: _ClassVar[int]
    PARAM_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[DataMeta]
    op: str
    param: _containers.ScalarMap[str, str]
    s: Session
    def __init__(self, op: _Optional[str] = ..., s: _Optional[_Union[Session, _Mapping]] = ..., param: _Optional[_Mapping[str, str]] = ..., data: _Optional[_Iterable[_Union[DataMeta, _Mapping]]] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ["body", "headers", "query"]
    BODY_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    body: str
    headers: str
    query: str
    def __init__(self, query: _Optional[str] = ..., headers: _Optional[str] = ..., body: _Optional[str] = ...) -> None: ...

class ResData(_message.Message):
    __slots__ = ["code", "data", "error_info", "param", "s"]
    class ParamEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    PARAM_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    code: int
    data: _containers.RepeatedCompositeFieldContainer[DataMeta]
    error_info: str
    param: _containers.ScalarMap[str, str]
    s: Session
    def __init__(self, code: _Optional[int] = ..., error_info: _Optional[str] = ..., s: _Optional[_Union[Session, _Mapping]] = ..., param: _Optional[_Mapping[str, str]] = ..., data: _Optional[_Iterable[_Union[DataMeta, _Mapping]]] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["body", "headers"]
    BODY_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    body: str
    headers: str
    def __init__(self, headers: _Optional[str] = ..., body: _Optional[str] = ...) -> None: ...

class Session(_message.Message):
    __slots__ = ["h", "sess", "t"]
    class SessEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    H_FIELD_NUMBER: _ClassVar[int]
    SESS_FIELD_NUMBER: _ClassVar[int]
    T_FIELD_NUMBER: _ClassVar[int]
    h: str
    sess: _containers.ScalarMap[str, str]
    t: str
    def __init__(self, t: _Optional[str] = ..., h: _Optional[str] = ..., sess: _Optional[_Mapping[str, str]] = ...) -> None: ...
