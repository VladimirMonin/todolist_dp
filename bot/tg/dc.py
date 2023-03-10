from dataclasses import dataclass, field
from typing import List, Optional, Type, ClassVar
from marshmallow import EXCLUDE, Schema


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]

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
class Entity:
    offset: int
    length: int
    type: str


@dataclass
class Message:
    message_id: int
    message_from: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat
    date: int
    text: str
    entities: Optional[List[Entity]]

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

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
    result: List[UpdateObj]

    class Meta:
        unknown = EXCLUDE

# @dataclass
# class GetUpdatesResponse:
#     """https://core.telegram.org/bots/api#getupdates"""
#     ok: bool
#     result: List[UpdateObj]
#
#     Schema: ClassVar[Type[Schema]] = Schema
#
#     class Meta:
#         unknown = EXCLUDE
#
#
# @dataclass
# class SendMessageResponse:
#     """https://core.telegram.org/bots/api#sendmessage"""
#     ok: bool
#     result: Message
#
#     Schema: ClassVar[Type[Schema]] = Schema
#
#     class Meta:
#         unknown = EXCLUDE
