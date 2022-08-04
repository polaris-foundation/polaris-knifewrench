from typing import Any, List

import pytest
from kombu import Consumer, Message
from kombu.mixins import ConsumerMixin

from dhos_knifewrench_adapter_worker import auth_token
from dhos_knifewrench_adapter_worker.knifewrench import ErrorQueueConsumer


@pytest.mark.usefixtures("knifewrench_200", "mock_api_jwt")
def test_consume_success(
    mocker: Any, error_message: Message, knifewrench_consumer: ErrorQueueConsumer
) -> None:
    mock_ack = mocker.patch.object(Message, "ack")
    knifewrench_consumer.on_message(body=b"", message=error_message)

    assert mock_ack.called_once


@pytest.mark.usefixtures("knifewrench_200", "mock_api_jwt")
def test_consume_success_string_body(
    mocker: Any, knifewrench_consumer: ErrorQueueConsumer
) -> None:
    message: Message = Message()
    message.headers = {
        "x-death": [
            {
                "time": "2019-06-11 12:50:56",
                "count": 1,
                "queue": "dhos-pdf-adapter-task-queue",
                "reason": "rejected",
                "exchange": "dhos",
                "routing-keys": ["dhos.DM000008"],
            }
        ],
        "x-first-death-queue": "dhos-pdf-adapter-task-queue",
        "x-first-death-reason": "rejected",
        "x-first-death-exchange": "dhos",
    }
    message.body = "Test message"
    mock_ack = mocker.patch.object(Message, "ack")
    knifewrench_consumer.on_message(body=b"", message=message)
    assert mock_ack.called_once


@pytest.mark.usefixtures("knifewrench_200", "mock_api_jwt")
def test_consume_success_no_headers(
    mocker: Any, knifewrench_consumer: ErrorQueueConsumer
) -> None:
    message: Message = Message()
    message.body = "Test message"
    mock_ack = mocker.patch.object(Message, "ack")
    knifewrench_consumer.on_message(body=b"", message=message)
    assert mock_ack.called_once


def test_consume_error(mocker: Any, knifewrench_consumer: ErrorQueueConsumer) -> None:
    mocker.patch.object(knifewrench_consumer, "_process_message", side_effect=Exception)
    message: Message = Message()
    mock_requeue = mocker.patch.object(Message, "requeue")
    knifewrench_consumer.on_message(body=b"", message=message)
    assert mock_requeue.called_once


@pytest.mark.usefixtures("knifewrench_503", "mock_api_jwt")
def test_consume_api_unavailable(
    mocker: Any, error_message: Message, knifewrench_consumer: ErrorQueueConsumer
) -> None:
    mock_requeue = mocker.patch.object(Message, "requeue")
    knifewrench_consumer.on_message(body=b"", message=error_message)
    assert mock_requeue.called_once


@pytest.mark.usefixtures("mock_api_jwt")
def test_jwt_success(systemauth_sample_jwt: str) -> None:

    _jwt = auth_token.get_api_jwt()
    assert _jwt == systemauth_sample_jwt


def test_consumers_registered(knifewrench_consumer: ErrorQueueConsumer) -> None:
    _consumers: List[ConsumerMixin] = knifewrench_consumer.get_consumers(Consumer, None)
    assert len(_consumers) == 1
