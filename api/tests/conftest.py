from typing import Dict, Generator

import pytest
from flask import Flask
from mock import Mock
from pytest_mock import MockFixture

from dhos_knifewrench_api.models import AmqpMessage


@pytest.fixture()
def app() -> Flask:
    """ "Fixture that creates app for testing"""
    from dhos_knifewrench_api.app import create_app

    return create_app(testing=True)


@pytest.fixture
def app_context(app: Flask) -> Generator[None, None, None]:
    with app.app_context():
        yield


@pytest.fixture
def mock_bearer_validation(mocker: MockFixture) -> Mock:
    from jose import jwt

    mocked = mocker.patch.object(jwt, "get_unverified_claims")
    mocked.return_value = {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": 1_516_239_022,
        "iss": "http://localhost/",
    }
    return mocked


@pytest.fixture
def amqp_message_in_dict() -> Dict:
    """Sample AMQP message as it comes from RabbitMQ"""
    return {
        "routing_key": "route.123",
        "headers": {
            "x-first-death-queue": "some-queue",
            "x-first-death-reason": "rejected",
            "x-first-death-exchange": "dhos",
            "x-death": [
                {
                    "time": "2019-01-14 12:52:47",
                    "count": 1,
                    "queue": "dhos-rules-adapter-task-queue",
                    "reason": "rejected",
                    "exchange": "dhos",
                    "routing-keys": ["route.123"],
                }
            ],
        },
        "body": {
            "a_sample_key": "a sample value!",
            "a_sample_key2": "another sample value!",
        },
        "raw_body": '{"a_sample_key": "a sample value!", "a_sample_key2": "another sample value!"}',
        "uuid": "fake-uuid",
    }


@pytest.fixture
def amqp_message_out_dict() -> Dict:
    """Sample AMQP message as a dict as it comes out of the API"""
    return {
        "routing_key": "route.123",
        "message_headers": {
            "x-first-death-queue": "some-queue",
            "x-first-death-reason": "rejected",
            "x-first-death-exchange": "dhos",
            "x-death": [
                {
                    "time": "2019-01-14 12:52:47",
                    "count": 1,
                    "queue": "dhos-rules-adapter-task-queue",
                    "reason": "rejected",
                    "exchange": "dhos",
                    "routing-keys": ["route.123"],
                }
            ],
        },
        "message_body": {
            "a_sample_key": "a sample value!",
            "a_sample_key2": "another sample value!",
        },
        "uuid": "fake-uuid",
    }


@pytest.fixture
def amqp_message_model() -> AmqpMessage:
    amqp_message = AmqpMessage()
    amqp_message.routing_key = "test.123"
    amqp_message.message_raw_body = "123"
    amqp_message.message_body = {"some": "body"}
    return amqp_message
