from v4_proto.dydxprotocol.delaymsg import delayed_message_pb2 as _delayed_message_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ["delayed_messages", "num_messages"]
    DELAYED_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    NUM_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    delayed_messages: _containers.RepeatedCompositeFieldContainer[_delayed_message_pb2.DelayedMessage]
    num_messages: int
    def __init__(self, delayed_messages: _Optional[_Iterable[_Union[_delayed_message_pb2.DelayedMessage, _Mapping]]] = ..., num_messages: _Optional[int] = ...) -> None: ...
