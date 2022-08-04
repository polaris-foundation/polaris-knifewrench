import json
import time
import uuid
from typing import Dict, Optional

from behave import given, then, when
from behave.runner import Context
from clients import dhos_client, rabbitmq_client
from kombu import Message
from requests import Response


@given("RabbitMQ is running")
def check_rabbitmq_running(context: Context) -> None:
    if not hasattr(context, "rabbit_connection"):
        rabbitmq_client.create_rabbitmq_infrastructure(context)


@given("I am authorised to talk to the API")
def get_system_jwt(context: Context) -> None:
    context.valid_amqp_jwt = dhos_client.get_system_token()


@given("an errored AMQP message is in knifewrench")
def create_amqp_message_in_knifewrench(context: Context) -> None:
    message_body = {"some": "body", "some_id": str(uuid.uuid4())}
    message_details = {
        "routing_key": "dhos.999",
        "body": message_body,
        "raw_body": json.dumps(message_body),
        "headers": {
            "x-first-death-exchange": "dhos",
            "x-first-death-reason": "test",
            "x-first-death-queue": "some-nonexistent-queue",
        },
    }
    response: Response = dhos_client.create_amqp_message(
        message_details=message_details, jwt=context.valid_amqp_jwt
    )
    assert response.status_code == 201
    context.existing_message_body = message_body
    context.existing_message_uuid = response.headers["Location"].split("/")[-1]


@when("I publish a test message with a string body to the error queue")
def publish_test_message(context: Context) -> None:
    message_identifier = str(uuid.uuid4())
    message_body: str = "test message contents"
    context.message_identifier = message_identifier
    rabbitmq_client.publish_message(
        connection=context.rabbit_connection,
        exchange=context.rabbit_exchange,
        routing_key="dhos.123",
        body=message_body,
        message_identifier=message_identifier,
    )


@when("a message is published to the error queue")
def publish_typical_dhos_message(context: Context) -> None:
    message_identifier = str(uuid.uuid4())
    message_body: str = json.dumps(
        {"a_sample_key": "a sample value!", "a_sample_key2": "another sample value!"}
    )
    context.message_identifier = message_identifier
    rabbitmq_client.publish_message(
        connection=context.rabbit_connection,
        exchange=context.rabbit_exchange,
        routing_key="dhos.123",
        body=message_body,
        message_identifier=message_identifier,
    )


@when("{seconds:d} seconds have passed")
def wait(context: Context, seconds: int) -> None:
    time.sleep(seconds)


@when("I republish the AMQP message")
def republish_message(context: Context) -> None:
    response: Response = dhos_client.republish_amqp_message(
        uuid=context.existing_message_uuid, jwt=context.valid_amqp_jwt
    )
    assert response.status_code == 204


@then("I see that the message has been saved")
def check_message_saved(context: Context) -> None:
    matching_message: Optional[Dict] = _get_amqp_message_by_message_identifier(
        message_identifier=context.message_identifier, jwt=context.valid_amqp_jwt
    )
    assert matching_message is not None
    context.amqp_message = matching_message


@then("I can look up the message by UUID")
def look_up_first_message(context: Context) -> None:
    message_uuid: str = context.amqp_message["uuid"]
    response = dhos_client.get_amqp_message(
        uuid=message_uuid, jwt=context.valid_amqp_jwt
    )
    assert response.status_code == 200


def _get_amqp_message_by_message_identifier(
    message_identifier: str, jwt: str
) -> Optional[Dict]:
    response: Response = dhos_client.get_all_amqp_messages(jwt=jwt)
    messages = response.json()
    return next(
        (
            m
            for m in messages
            if m["message_headers"].get("x-message-identifier") == message_identifier
        ),
        None,
    )


@then("I see that the message has been published to rabbitmq")
def check_message_sent_to_rabbitmq(context: Context) -> None:
    message: Message = rabbitmq_client.get_message_on_queue(
        context.destination_queue, context
    )
    assert json.loads(message.body) == context.existing_message_body
