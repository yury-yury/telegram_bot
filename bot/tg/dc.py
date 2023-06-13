import json
from dataclasses import field

from marshmallow_dataclass import dataclass
from marshmallow import EXCLUDE, Schema
from typing import List, ClassVar, Type, Optional


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: Optional[str]
    username: Optional[str]

    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat:
    id: int
    first_name: Optional[str]
    username: Optional[str]
    type: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    message_id: int
    date: int
    text: Optional[str]
    from_: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Message

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj] = field(default_factory=list)

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE
