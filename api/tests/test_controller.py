import uuid
from typing import Dict
from unittest.mock import MagicMock

import kombu_batteries_included
import pytest
from flask_batteries_included.helpers.error_handler import EntityNotFoundException
from flask_batteries_included.sqldb import db
from mock import Mock
from pytest_mock import MockFixture
from sqlalchemy.sql.elements import BinaryExpression

from dhos_knifewrench_api.api import controller
from dhos_knifewrench_api.models import AmqpMessage


@pytest.mark.usefixtures("app")
class TestController:
    def test_create_amqp_message(
        self, mocker: MockFixture, amqp_message_in_dict: Dict
    ) -> None:
        """Test a successful object creation"""

        # Mock the session add
        mock_session_add: MagicMock = mocker.patch.object(db.session, "add")

        # Make the call
        controller.create(amqp_message_in_dict)

        # Extract the AmqpMessage that create() made, and to_dict() it
        assert mock_session_add.called_once
        amqp_message: AmqpMessage = mock_session_add.call_args[0][0]
        amqp_to_dict: Dict = amqp_message.to_dict()

        # Make sure the status is defaulted correctly
        assert amqp_to_dict["status"] == "new"

        # Make sure the inputs have come out
        assert amqp_to_dict["routing_key"] == amqp_message_in_dict["routing_key"]
        assert amqp_to_dict["message_headers"] == amqp_message_in_dict["headers"]
        assert amqp_to_dict["message_body"] == amqp_message_in_dict["body"]

    def test_create_amqp_message_list(self, mocker: MockFixture) -> None:
        # Mock the session add
        mock_session_add: MagicMock = mocker.patch.object(db.session, "add")

        # Make the call
        controller.create(
            {
                "routing_key": None,
                "body": [],
                "headers": {},
                "raw_body": "this is a body",
            }
        )

        # Extract the AmqpMessage that create() made, and to_dict() it
        assert mock_session_add.called_once
        amqp_message: AmqpMessage = mock_session_add.call_args[0][0]
        amqp_to_dict: Dict = amqp_message.to_dict()

        # Make sure the status is defaulted correctly
        assert amqp_to_dict["status"] == "new"

        # Make sure the inputs have come out
        assert amqp_to_dict["routing_key"] is None
        assert amqp_to_dict["message_headers"] == {}
        assert amqp_to_dict["message_body"] == []

    def test_list_amqp_messages(self, mocker: MockFixture) -> None:
        # Set up expected filter
        status_filter: str = "test_filter"
        expected_filter: BinaryExpression = AmqpMessage.status == status_filter

        # Mock the query call
        mock_q: MagicMock = mocker.patch.object(AmqpMessage, "query")

        # Make the call
        controller.get_list(status_filter=status_filter)

        # Make sure the filter was applied
        assert expected_filter.compare(mock_q.filter.call_args[0][0])

    def test_get_amqp_message(self, mocker: MockFixture) -> None:
        # Set up fake UUID
        fake_uuid: str = str(uuid.uuid4())
        expected_filter: BinaryExpression = AmqpMessage.uuid == fake_uuid

        # Mock the query call
        mock_q: MagicMock = mocker.patch.object(AmqpMessage, "query")

        # Make the call
        controller.get_message(message_uuid=fake_uuid)

        # Make sure the uuid was sent in
        assert expected_filter.compare(mock_q.filter.call_args[0][0])

    def test_get_amqp_message_not_found(self, mocker: MockFixture) -> None:
        # Mock the query call
        mock_q: MagicMock = mocker.patch.object(AmqpMessage, "query")

        # Mock the response as though an entity isn't found
        mocked_filter: MagicMock = MagicMock()
        mocked_filter.first.return_value = None
        mock_q.filter.return_value = mocked_filter

        # Make the call
        with pytest.raises(EntityNotFoundException):
            controller.get_message(message_uuid="12345")

    def test_republish_amqp_message(
        self, mocker: MockFixture, amqp_message_model: AmqpMessage
    ) -> None:
        # Set up fake UUID
        fake_uuid: str = amqp_message_model.uuid
        expected_filter: BinaryExpression = AmqpMessage.uuid == fake_uuid

        mock_publish: Mock = mocker.patch.object(
            kombu_batteries_included, "publish_message"
        )

        # Mock the query call
        amqp_message_model.message_headers = {"x-first-death-exchange": "dhos"}
        mock_q: MagicMock = mocker.patch.object(AmqpMessage, "query")
        mocked_filter: MagicMock = MagicMock()
        mocked_filter.first.return_value = amqp_message_model
        mock_q.filter.return_value = mocked_filter

        # Make the call
        controller.republish_message(message_uuid=fake_uuid)

        # Make sure the uuid was sent in
        assert expected_filter.compare(mock_q.filter.call_args[0][0])
        assert mock_publish.call_count == 1
        mock_publish.assert_called_with(
            routing_key=amqp_message_model.routing_key,
            body=amqp_message_model.message_body,
            headers=amqp_message_model.message_headers,
        )

    def test_republish_multiple_amqp_messages(
        self, mocker: MockFixture, amqp_message_model: AmqpMessage
    ) -> None:
        # Set up fake UUID
        fake_uuid: str = amqp_message_model.uuid
        expected_filter: BinaryExpression = AmqpMessage.uuid.in_([fake_uuid])

        mock_publish: Mock = mocker.patch.object(
            kombu_batteries_included, "publish_message"
        )

        # Mock the query call
        amqp_message_model.message_headers = {"x-first-death-exchange": "dhos"}
        mock_q: MagicMock = mocker.patch.object(AmqpMessage, "query")
        mocked_filter: MagicMock = MagicMock()
        mocked_filter.all.return_value = [amqp_message_model]
        mock_q.filter.return_value = mocked_filter

        # Make the call
        controller.republish_multiple_messages(message_uuids=[fake_uuid])

        # Make sure the uuid was sent in
        assert expected_filter.compare(mock_q.filter.call_args[0][0])
        assert mock_publish.call_count == 1
        mock_publish.assert_called_with(
            routing_key=amqp_message_model.routing_key,
            body=amqp_message_model.message_body,
            headers=amqp_message_model.message_headers,
        )

    def test_republish_multiple_amqp_messages_no_xdeath(
        self, mocker: MockFixture, amqp_message_model: AmqpMessage
    ) -> None:
        # Set up fake UUID
        fake_uuid: str = amqp_message_model.uuid

        # Mock the query call
        mock_q: MagicMock = mocker.patch.object(AmqpMessage, "query")
        mocked_filter: MagicMock = MagicMock()
        mocked_filter.all.return_value = [amqp_message_model]
        mock_q.filter.return_value = mocked_filter

        # Make the call
        with pytest.raises(ValueError):
            controller.republish_multiple_messages(message_uuids=[fake_uuid])
