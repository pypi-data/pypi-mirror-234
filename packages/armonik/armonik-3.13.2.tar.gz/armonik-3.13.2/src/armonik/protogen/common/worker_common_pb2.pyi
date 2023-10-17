from . import objects_pb2 as _objects_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProcessRequest(_message.Message):
    __slots__ = ["communication_token", "compute"]
    class ComputeRequest(_message.Message):
        __slots__ = ["init_request", "payload", "init_data", "data"]
        class InitRequest(_message.Message):
            __slots__ = ["configuration", "session_id", "task_id", "task_options", "expected_output_keys", "payload"]
            CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
            SESSION_ID_FIELD_NUMBER: _ClassVar[int]
            TASK_ID_FIELD_NUMBER: _ClassVar[int]
            TASK_OPTIONS_FIELD_NUMBER: _ClassVar[int]
            EXPECTED_OUTPUT_KEYS_FIELD_NUMBER: _ClassVar[int]
            PAYLOAD_FIELD_NUMBER: _ClassVar[int]
            configuration: _objects_pb2.Configuration
            session_id: str
            task_id: str
            task_options: _objects_pb2.TaskOptions
            expected_output_keys: _containers.RepeatedScalarFieldContainer[str]
            payload: _objects_pb2.DataChunk
            def __init__(self, configuration: _Optional[_Union[_objects_pb2.Configuration, _Mapping]] = ..., session_id: _Optional[str] = ..., task_id: _Optional[str] = ..., task_options: _Optional[_Union[_objects_pb2.TaskOptions, _Mapping]] = ..., expected_output_keys: _Optional[_Iterable[str]] = ..., payload: _Optional[_Union[_objects_pb2.DataChunk, _Mapping]] = ...) -> None: ...
        class InitData(_message.Message):
            __slots__ = ["key", "last_data"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            LAST_DATA_FIELD_NUMBER: _ClassVar[int]
            key: str
            last_data: bool
            def __init__(self, key: _Optional[str] = ..., last_data: bool = ...) -> None: ...
        INIT_REQUEST_FIELD_NUMBER: _ClassVar[int]
        PAYLOAD_FIELD_NUMBER: _ClassVar[int]
        INIT_DATA_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        init_request: ProcessRequest.ComputeRequest.InitRequest
        payload: _objects_pb2.DataChunk
        init_data: ProcessRequest.ComputeRequest.InitData
        data: _objects_pb2.DataChunk
        def __init__(self, init_request: _Optional[_Union[ProcessRequest.ComputeRequest.InitRequest, _Mapping]] = ..., payload: _Optional[_Union[_objects_pb2.DataChunk, _Mapping]] = ..., init_data: _Optional[_Union[ProcessRequest.ComputeRequest.InitData, _Mapping]] = ..., data: _Optional[_Union[_objects_pb2.DataChunk, _Mapping]] = ...) -> None: ...
    COMMUNICATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_FIELD_NUMBER: _ClassVar[int]
    communication_token: str
    compute: ProcessRequest.ComputeRequest
    def __init__(self, communication_token: _Optional[str] = ..., compute: _Optional[_Union[ProcessRequest.ComputeRequest, _Mapping]] = ...) -> None: ...

class ProcessReply(_message.Message):
    __slots__ = ["communication_token", "output"]
    COMMUNICATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    communication_token: str
    output: _objects_pb2.Output
    def __init__(self, communication_token: _Optional[str] = ..., output: _Optional[_Union[_objects_pb2.Output, _Mapping]] = ...) -> None: ...

class HealthCheckReply(_message.Message):
    __slots__ = ["status"]
    class ServingStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        UNKNOWN: _ClassVar[HealthCheckReply.ServingStatus]
        SERVING: _ClassVar[HealthCheckReply.ServingStatus]
        NOT_SERVING: _ClassVar[HealthCheckReply.ServingStatus]
    UNKNOWN: HealthCheckReply.ServingStatus
    SERVING: HealthCheckReply.ServingStatus
    NOT_SERVING: HealthCheckReply.ServingStatus
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: HealthCheckReply.ServingStatus
    def __init__(self, status: _Optional[_Union[HealthCheckReply.ServingStatus, str]] = ...) -> None: ...
