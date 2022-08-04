from enum import Enum

from .amqp_message import AmqpMessage


class MessageStatus(Enum):
    NEW = "new"
    ARCHIVED = "archived"
    REPUBLISHED = "republished"


__all__ = ["AmqpMessage", "MessageStatus"]
