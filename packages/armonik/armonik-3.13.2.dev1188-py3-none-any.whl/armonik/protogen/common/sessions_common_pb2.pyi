from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from . import objects_pb2 as _objects_pb2
from . import session_status_pb2 as _session_status_pb2
from . import sessions_fields_pb2 as _sessions_fields_pb2
from . import sessions_filters_pb2 as _sessions_filters_pb2
from . import sort_direction_pb2 as _sort_direction_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SessionRaw(_message.Message):
    __slots__ = ["session_id", "status", "partition_ids", "options", "created_at", "cancelled_at", "duration"]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PARTITION_IDS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CANCELLED_AT_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    status: _session_status_pb2.SessionStatus
    partition_ids: _containers.RepeatedScalarFieldContainer[str]
    options: _objects_pb2.TaskOptions
    created_at: _timestamp_pb2.Timestamp
    cancelled_at: _timestamp_pb2.Timestamp
    duration: _duration_pb2.Duration
    def __init__(self, session_id: _Optional[str] = ..., status: _Optional[_Union[_session_status_pb2.SessionStatus, str]] = ..., partition_ids: _Optional[_Iterable[str]] = ..., options: _Optional[_Union[_objects_pb2.TaskOptions, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., cancelled_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class ListSessionsRequest(_message.Message):
    __slots__ = ["page", "page_size", "filters", "sort", "with_task_options"]
    class Sort(_message.Message):
        __slots__ = ["field", "direction"]
        FIELD_FIELD_NUMBER: _ClassVar[int]
        DIRECTION_FIELD_NUMBER: _ClassVar[int]
        field: _sessions_fields_pb2.SessionField
        direction: _sort_direction_pb2.SortDirection
        def __init__(self, field: _Optional[_Union[_sessions_fields_pb2.SessionField, _Mapping]] = ..., direction: _Optional[_Union[_sort_direction_pb2.SortDirection, str]] = ...) -> None: ...
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    WITH_TASK_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    filters: _sessions_filters_pb2.Filters
    sort: ListSessionsRequest.Sort
    with_task_options: bool
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ..., filters: _Optional[_Union[_sessions_filters_pb2.Filters, _Mapping]] = ..., sort: _Optional[_Union[ListSessionsRequest.Sort, _Mapping]] = ..., with_task_options: bool = ...) -> None: ...

class ListSessionsResponse(_message.Message):
    __slots__ = ["sessions", "page", "page_size", "total"]
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    sessions: _containers.RepeatedCompositeFieldContainer[SessionRaw]
    page: int
    page_size: int
    total: int
    def __init__(self, sessions: _Optional[_Iterable[_Union[SessionRaw, _Mapping]]] = ..., page: _Optional[int] = ..., page_size: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...

class GetSessionRequest(_message.Message):
    __slots__ = ["session_id"]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class GetSessionResponse(_message.Message):
    __slots__ = ["session"]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    session: SessionRaw
    def __init__(self, session: _Optional[_Union[SessionRaw, _Mapping]] = ...) -> None: ...

class CancelSessionRequest(_message.Message):
    __slots__ = ["session_id"]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class CancelSessionResponse(_message.Message):
    __slots__ = ["session"]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    session: SessionRaw
    def __init__(self, session: _Optional[_Union[SessionRaw, _Mapping]] = ...) -> None: ...

class CreateSessionRequest(_message.Message):
    __slots__ = ["default_task_option", "partition_ids"]
    DEFAULT_TASK_OPTION_FIELD_NUMBER: _ClassVar[int]
    PARTITION_IDS_FIELD_NUMBER: _ClassVar[int]
    default_task_option: _objects_pb2.TaskOptions
    partition_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, default_task_option: _Optional[_Union[_objects_pb2.TaskOptions, _Mapping]] = ..., partition_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateSessionReply(_message.Message):
    __slots__ = ["session_id"]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...
