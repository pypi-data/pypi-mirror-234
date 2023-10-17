from v4_proto.cosmos_proto import cosmos_pb2 as _cosmos_pb2
from v4_proto.cosmos.msg.v1 import msg_pb2 as _msg_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from v4_proto.dydxprotocol.blocktime import params_pb2 as _params_pb2
from v4_proto.gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgUpdateDowntimeParams(_message.Message):
    __slots__ = ["authority", "params"]
    AUTHORITY_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    authority: str
    params: _params_pb2.DowntimeParams
    def __init__(self, authority: _Optional[str] = ..., params: _Optional[_Union[_params_pb2.DowntimeParams, _Mapping]] = ...) -> None: ...

class MsgUpdateDowntimeParamsResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgIsDelayedBlock(_message.Message):
    __slots__ = ["delay_duration"]
    DELAY_DURATION_FIELD_NUMBER: _ClassVar[int]
    delay_duration: _duration_pb2.Duration
    def __init__(self, delay_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class MsgIsDelayedBlockResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
