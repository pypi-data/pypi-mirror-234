import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SendTaskRequest(_message.Message):
    __slots__ = ["input_files", "task"]
    INPUT_FILES_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    input_files: _containers.RepeatedScalarFieldContainer[str]
    task: str
    def __init__(self, input_files: _Optional[_Iterable[str]] = ..., task: _Optional[str] = ...) -> None: ...

class OnAgentAction(_message.Message):
    __slots__ = ["input", "tool"]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    TOOL_FIELD_NUMBER: _ClassVar[int]
    input: str
    tool: str
    def __init__(self, input: _Optional[str] = ..., tool: _Optional[str] = ...) -> None: ...

class OnAgentActionEnd(_message.Message):
    __slots__ = ["output", "output_files", "has_error"]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FILES_FIELD_NUMBER: _ClassVar[int]
    HAS_ERROR_FIELD_NUMBER: _ClassVar[int]
    output: str
    output_files: _containers.RepeatedScalarFieldContainer[str]
    has_error: bool
    def __init__(self, output: _Optional[str] = ..., output_files: _Optional[_Iterable[str]] = ..., has_error: bool = ...) -> None: ...

class FinalRespond(_message.Message):
    __slots__ = ["answer"]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    answer: str
    def __init__(self, answer: _Optional[str] = ...) -> None: ...

class TaskState(_message.Message):
    __slots__ = ["generated_token_count", "iteration_count", "model_name", "total_duration", "sent_token_count", "model_respond_duration"]
    GENERATED_TOKEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    ITERATION_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DURATION_FIELD_NUMBER: _ClassVar[int]
    SENT_TOKEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODEL_RESPOND_DURATION_FIELD_NUMBER: _ClassVar[int]
    generated_token_count: int
    iteration_count: int
    model_name: str
    total_duration: int
    sent_token_count: int
    model_respond_duration: int
    def __init__(self, generated_token_count: _Optional[int] = ..., iteration_count: _Optional[int] = ..., model_name: _Optional[str] = ..., total_duration: _Optional[int] = ..., sent_token_count: _Optional[int] = ..., model_respond_duration: _Optional[int] = ...) -> None: ...

class TaskRespond(_message.Message):
    __slots__ = ["state", "respond_type", "on_agent_action", "on_agent_action_end", "final_respond", "console_stdout", "console_stderr", "typing_content"]
    class RespondType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        OnAgentActionType: _ClassVar[TaskRespond.RespondType]
        OnAgentActionStdout: _ClassVar[TaskRespond.RespondType]
        OnAgentActionStderr: _ClassVar[TaskRespond.RespondType]
        OnAgentActionEndType: _ClassVar[TaskRespond.RespondType]
        OnFinalAnswerType: _ClassVar[TaskRespond.RespondType]
        OnAgentTextTyping: _ClassVar[TaskRespond.RespondType]
        OnAgentCodeTyping: _ClassVar[TaskRespond.RespondType]
    OnAgentActionType: TaskRespond.RespondType
    OnAgentActionStdout: TaskRespond.RespondType
    OnAgentActionStderr: TaskRespond.RespondType
    OnAgentActionEndType: TaskRespond.RespondType
    OnFinalAnswerType: TaskRespond.RespondType
    OnAgentTextTyping: TaskRespond.RespondType
    OnAgentCodeTyping: TaskRespond.RespondType
    STATE_FIELD_NUMBER: _ClassVar[int]
    RESPOND_TYPE_FIELD_NUMBER: _ClassVar[int]
    ON_AGENT_ACTION_FIELD_NUMBER: _ClassVar[int]
    ON_AGENT_ACTION_END_FIELD_NUMBER: _ClassVar[int]
    FINAL_RESPOND_FIELD_NUMBER: _ClassVar[int]
    CONSOLE_STDOUT_FIELD_NUMBER: _ClassVar[int]
    CONSOLE_STDERR_FIELD_NUMBER: _ClassVar[int]
    TYPING_CONTENT_FIELD_NUMBER: _ClassVar[int]
    state: TaskState
    respond_type: TaskRespond.RespondType
    on_agent_action: OnAgentAction
    on_agent_action_end: OnAgentActionEnd
    final_respond: FinalRespond
    console_stdout: str
    console_stderr: str
    typing_content: str
    def __init__(self, state: _Optional[_Union[TaskState, _Mapping]] = ..., respond_type: _Optional[_Union[TaskRespond.RespondType, str]] = ..., on_agent_action: _Optional[_Union[OnAgentAction, _Mapping]] = ..., on_agent_action_end: _Optional[_Union[OnAgentActionEnd, _Mapping]] = ..., final_respond: _Optional[_Union[FinalRespond, _Mapping]] = ..., console_stdout: _Optional[str] = ..., console_stderr: _Optional[str] = ..., typing_content: _Optional[str] = ...) -> None: ...

class AddKernelRequest(_message.Message):
    __slots__ = ["endpoint", "key"]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    endpoint: str
    key: str
    def __init__(self, endpoint: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class AddKernelResponse(_message.Message):
    __slots__ = ["code", "msg"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ...) -> None: ...

class AssembleAppRequest(_message.Message):
    __slots__ = ["name", "language", "code", "saved_filenames", "desc"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    SAVED_FILENAMES_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    name: str
    language: str
    code: str
    saved_filenames: _containers.RepeatedScalarFieldContainer[str]
    desc: str
    def __init__(self, name: _Optional[str] = ..., language: _Optional[str] = ..., code: _Optional[str] = ..., saved_filenames: _Optional[_Iterable[str]] = ..., desc: _Optional[str] = ...) -> None: ...

class AssembleAppResponse(_message.Message):
    __slots__ = ["code", "msg"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ...) -> None: ...

class RunAppRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class AppInfo(_message.Message):
    __slots__ = ["name", "language", "ctime", "desc"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    CTIME_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    name: str
    language: str
    ctime: int
    desc: str
    def __init__(self, name: _Optional[str] = ..., language: _Optional[str] = ..., ctime: _Optional[int] = ..., desc: _Optional[str] = ...) -> None: ...

class QueryAppsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class QueryAppsResponse(_message.Message):
    __slots__ = ["apps"]
    APPS_FIELD_NUMBER: _ClassVar[int]
    apps: _containers.RepeatedCompositeFieldContainer[AppInfo]
    def __init__(self, apps: _Optional[_Iterable[_Union[AppInfo, _Mapping]]] = ...) -> None: ...

class PingRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PongResponse(_message.Message):
    __slots__ = ["code", "msg"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ...) -> None: ...
