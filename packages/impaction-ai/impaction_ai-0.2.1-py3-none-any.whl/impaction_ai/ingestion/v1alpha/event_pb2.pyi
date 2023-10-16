from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Event(_message.Message):
    __slots__ = ["id", "type", "create_time", "properties", "project_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    create_time: _timestamp_pb2.Timestamp
    properties: EventProperties
    project_id: str
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., properties: _Optional[_Union[EventProperties, _Mapping]] = ..., project_id: _Optional[str] = ...) -> None: ...

class EventProperties(_message.Message):
    __slots__ = ["session_properties", "message_properties", "user_properties", "feedback_properties"]
    class SessionProperties(_message.Message):
        __slots__ = ["session_id", "session_title", "session_start_time", "user_id", "assistant_id"]
        SESSION_ID_FIELD_NUMBER: _ClassVar[int]
        SESSION_TITLE_FIELD_NUMBER: _ClassVar[int]
        SESSION_START_TIME_FIELD_NUMBER: _ClassVar[int]
        USER_ID_FIELD_NUMBER: _ClassVar[int]
        ASSISTANT_ID_FIELD_NUMBER: _ClassVar[int]
        session_id: str
        session_title: str
        session_start_time: _timestamp_pb2.Timestamp
        user_id: str
        assistant_id: str
        def __init__(self, session_id: _Optional[str] = ..., session_title: _Optional[str] = ..., session_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., user_id: _Optional[str] = ..., assistant_id: _Optional[str] = ...) -> None: ...
    class MessageProperties(_message.Message):
        __slots__ = ["session_id", "message_id_hint", "message_index_hint", "message_role", "message_content", "message_create_time"]
        class Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            ROLE_UNSPECIFIED: _ClassVar[EventProperties.MessageProperties.Role]
            ROLE_USER: _ClassVar[EventProperties.MessageProperties.Role]
            ROLE_ASSISTANT: _ClassVar[EventProperties.MessageProperties.Role]
        ROLE_UNSPECIFIED: EventProperties.MessageProperties.Role
        ROLE_USER: EventProperties.MessageProperties.Role
        ROLE_ASSISTANT: EventProperties.MessageProperties.Role
        SESSION_ID_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_ID_HINT_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_INDEX_HINT_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_ROLE_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_CONTENT_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
        session_id: str
        message_id_hint: str
        message_index_hint: int
        message_role: EventProperties.MessageProperties.Role
        message_content: str
        message_create_time: _timestamp_pb2.Timestamp
        def __init__(self, session_id: _Optional[str] = ..., message_id_hint: _Optional[str] = ..., message_index_hint: _Optional[int] = ..., message_role: _Optional[_Union[EventProperties.MessageProperties.Role, str]] = ..., message_content: _Optional[str] = ..., message_create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    class UserProperties(_message.Message):
        __slots__ = ["user_id", "user_email", "user_ip", "user_location", "user_create_time", "user_display_name"]
        class Location(_message.Message):
            __slots__ = ["country_code", "state", "city"]
            COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
            STATE_FIELD_NUMBER: _ClassVar[int]
            CITY_FIELD_NUMBER: _ClassVar[int]
            country_code: str
            state: str
            city: str
            def __init__(self, country_code: _Optional[str] = ..., state: _Optional[str] = ..., city: _Optional[str] = ...) -> None: ...
        USER_ID_FIELD_NUMBER: _ClassVar[int]
        USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
        USER_IP_FIELD_NUMBER: _ClassVar[int]
        USER_LOCATION_FIELD_NUMBER: _ClassVar[int]
        USER_CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
        USER_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
        user_id: str
        user_email: str
        user_ip: str
        user_location: EventProperties.UserProperties.Location
        user_create_time: _timestamp_pb2.Timestamp
        user_display_name: str
        def __init__(self, user_id: _Optional[str] = ..., user_email: _Optional[str] = ..., user_ip: _Optional[str] = ..., user_location: _Optional[_Union[EventProperties.UserProperties.Location, _Mapping]] = ..., user_create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., user_display_name: _Optional[str] = ...) -> None: ...
    class FeedbackProperties(_message.Message):
        __slots__ = ["session_id", "feedback_target", "feedback_score", "message_id_hint", "message_index_hint"]
        class Target(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            TARGET_UNSPECIFIED: _ClassVar[EventProperties.FeedbackProperties.Target]
            TARGET_SESSION: _ClassVar[EventProperties.FeedbackProperties.Target]
            TARGET_MESSAGE: _ClassVar[EventProperties.FeedbackProperties.Target]
        TARGET_UNSPECIFIED: EventProperties.FeedbackProperties.Target
        TARGET_SESSION: EventProperties.FeedbackProperties.Target
        TARGET_MESSAGE: EventProperties.FeedbackProperties.Target
        SESSION_ID_FIELD_NUMBER: _ClassVar[int]
        FEEDBACK_TARGET_FIELD_NUMBER: _ClassVar[int]
        FEEDBACK_SCORE_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_ID_HINT_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_INDEX_HINT_FIELD_NUMBER: _ClassVar[int]
        session_id: str
        feedback_target: EventProperties.FeedbackProperties.Target
        feedback_score: int
        message_id_hint: str
        message_index_hint: int
        def __init__(self, session_id: _Optional[str] = ..., feedback_target: _Optional[_Union[EventProperties.FeedbackProperties.Target, str]] = ..., feedback_score: _Optional[int] = ..., message_id_hint: _Optional[str] = ..., message_index_hint: _Optional[int] = ...) -> None: ...
    SESSION_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    USER_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    session_properties: EventProperties.SessionProperties
    message_properties: EventProperties.MessageProperties
    user_properties: EventProperties.UserProperties
    feedback_properties: EventProperties.FeedbackProperties
    def __init__(self, session_properties: _Optional[_Union[EventProperties.SessionProperties, _Mapping]] = ..., message_properties: _Optional[_Union[EventProperties.MessageProperties, _Mapping]] = ..., user_properties: _Optional[_Union[EventProperties.UserProperties, _Mapping]] = ..., feedback_properties: _Optional[_Union[EventProperties.FeedbackProperties, _Mapping]] = ...) -> None: ...
