from t2iapi import basic_responses_pb2 as _basic_responses_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRemovableDescriptorsResponse(_message.Message):
    __slots__ = ["status", "handle"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    status: _basic_responses_pb2.BasicResponse
    handle: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, status: _Optional[_Union[_basic_responses_pb2.BasicResponse, _Mapping]] = ..., handle: _Optional[_Iterable[str]] = ...) -> None: ...

class InsertMdsDescriptorResponse(_message.Message):
    __slots__ = ["status", "handle"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    status: _basic_responses_pb2.BasicResponse
    handle: str
    def __init__(self, status: _Optional[_Union[_basic_responses_pb2.BasicResponse, _Mapping]] = ..., handle: _Optional[str] = ...) -> None: ...
