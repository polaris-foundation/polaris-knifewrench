from typing import Dict, List, Optional, Set

import kombu_batteries_included
from flask_batteries_included.helpers.error_handler import EntityNotFoundException
from flask_batteries_included.sqldb import db, generate_uuid
from she_logging import logger

from dhos_knifewrench_api.models import AmqpMessage, MessageStatus


def create(amqp_message: Dict) -> Dict:
    message_uuid: str = generate_uuid()
    logger.info("Creating new AMQP message with UUID '%s'", message_uuid)
    message: AmqpMessage = AmqpMessage()
    message.uuid = message_uuid
    message.routing_key = amqp_message["routing_key"]
    message.message_body = amqp_message["body"]
    message.message_raw_body = amqp_message["raw_body"]
    message.message_headers = amqp_message.get("headers", {})
    message.status = MessageStatus.NEW.value
    db.session.add(message)
    db.session.commit()
    logger.info("Saved message successfully with UUID '%s'", message_uuid)
    return message.to_dict()


def get_list(status_filter: str = None, limit: int = 50) -> List[Dict]:
    """Returns a list of errored messages, filtered by status. No message bodies included. Maximum of 50."""
    q = AmqpMessage.query
    if status_filter is not None:
        q = q.filter(AmqpMessage.status == status_filter)
    q = q.limit(limit)
    return [a.to_dict_no_body() for a in q]


def get_message(message_uuid: str) -> Dict:
    """Returns a single errored message, including its message body."""
    message: Optional[AmqpMessage] = AmqpMessage.query.filter(
        AmqpMessage.uuid == message_uuid
    ).first()
    if message is None:
        raise EntityNotFoundException(f"Message with UUID '{message_uuid}' not found")
    return message.to_dict()


def republish_message(message_uuid: str) -> None:
    message: AmqpMessage = AmqpMessage.query.filter(
        AmqpMessage.uuid == message_uuid
    ).first()
    if message is None:
        raise EntityNotFoundException(f"Message with UUID '{message_uuid}' not found")
    _check_message_republish(message)
    _republish_message(message)


def republish_multiple_messages(message_uuids: List[str]) -> None:
    logger.info("Republishing %d messages", len(message_uuids))
    messages: List[AmqpMessage] = AmqpMessage.query.filter(
        AmqpMessage.uuid.in_(message_uuids)
    ).all()
    # First check all requested messages exist so that we don't republish some and not others
    unknown_message_uuids: Set[str] = set(message_uuids) - {m.uuid for m in messages}
    if unknown_message_uuids:
        raise EntityNotFoundException(
            f"No messages have been republished, unknown UUIDs: {', '.join(unknown_message_uuids)}"
        )
    # Check all messages can be republished before we start trying.
    for message in messages:
        _check_message_republish(message)
    # Start republishing.
    for message in messages:
        _republish_message(message)


def _check_message_republish(message: AmqpMessage) -> None:
    if message.message_headers is None:
        raise ValueError(f"Cannot republish message, no headers")
    if (exchange := message.message_headers.get("x-first-death-exchange")) != "dhos":
        raise ValueError(
            f"Cannot republish message to unexpected exchange '{exchange}'"
        )
    if message.routing_key is None:
        raise ValueError(f"Cannot republish message, no routing key")
    if message.message_body is None:
        raise ValueError(f"Cannot republish message, no message body")


def _republish_message(message: AmqpMessage) -> None:
    message.status = MessageStatus.REPUBLISHED.value
    logger.info(
        "Republishing message %s with routing key %s", message.uuid, message.routing_key
    )
    kombu_batteries_included.publish_message(
        routing_key=message.routing_key,
        body=message.message_body,
        headers=message.message_headers,
    )
    db.session.commit()
