import uuid
from typing import Dict, List

import pytest
from flask.testing import FlaskClient
from mock import Mock
from pytest_mock import MockFixture

from dhos_knifewrench_api.api import controller


@pytest.mark.usefixtures("mock_bearer_validation")
class TestApi:
    def test_create_amqp_message_success(
        self, mocker: MockFixture, client: FlaskClient, amqp_message_in_dict: Dict
    ) -> None:
        """Test creating an AMQP message"""
        mock_create = mocker.patch.object(controller, "create")
        response = client.post(
            f"/dhos/v1/amqp_message",
            json=amqp_message_in_dict,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_create.called_once
        assert response.status_code == 201

    def test_create_amqp_message_additional_field(
        self, mocker: MockFixture, client: FlaskClient, amqp_message_in_dict: Dict
    ) -> None:
        """Test additional fields are just ignored"""
        mock_create = mocker.patch.object(controller, "create")
        response = client.post(
            f"/dhos/v1/amqp_message",
            json={**amqp_message_in_dict, "hello!": "world"},
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_create.called_once
        assert response.status_code == 201

    def test_create_amqp_message_array_body(
        self, mocker: MockFixture, client: FlaskClient
    ) -> None:
        mock_create = mocker.patch.object(controller, "create")
        payload = {
            "routing_key": "route.123",
            "body": [
                "a sample value!",
                "another sample value!",
            ],
            "raw_body": '["a sample value!", "another sample value!"]',
            "uuid": "fake-uuid",
        }
        response = client.post(
            f"/dhos/v1/amqp_message",
            json=payload,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_create.called_once
        assert response.status_code == 201

    def test_create_amqp_message_empty_payload(
        self, mocker: MockFixture, client: FlaskClient
    ) -> None:
        """Test empty doesn't work"""
        mock_create = mocker.patch.object(controller, "create")
        response = client.post(
            f"/dhos/v1/amqp_message", json={}, headers={"Authorization": "Bearer TOKEN"}
        )
        assert mock_create.called_once
        assert response.status_code == 400

    def test_create_amqp_message_no_raw_body(
        self, mocker: MockFixture, client: FlaskClient, amqp_message_in_dict: Dict
    ) -> None:
        """Test missing raw body doesn't work"""
        mock_create = mocker.patch.object(controller, "create")
        response = client.post(
            f"/dhos/v1/amqp_message",
            json={k: v for k, v in amqp_message_in_dict.items() if k != "raw_body"},
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_create.called_once
        assert response.status_code == 400

    def test_create_amqp_message_no_content_type(
        self, mocker: MockFixture, client: FlaskClient, amqp_message_in_dict: Dict
    ) -> None:
        """Test wrong content-type doesn't work"""
        mock_create = mocker.patch.object(controller, "create")
        response = client.post(
            f"/dhos/v1/amqp_message",
            data={"routing_key": amqp_message_in_dict["routing_key"]},
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_create.called_once
        assert response.status_code == 415

    def test_create_amqp_message_no_auth(
        self, client: FlaskClient, amqp_message_in_dict: Dict
    ) -> None:
        response = client.post(
            f"/dhos/v1/amqp_message",
            json=amqp_message_in_dict,
        )
        assert response.status_code == 401

    def test_list_amqp_message_success(
        self, mocker: MockFixture, client: FlaskClient, amqp_message_in_dict: Dict
    ) -> None:
        """Test listing AMQP messages"""
        mock_get_list = mocker.patch.object(
            controller,
            "get_list",
            return_value=[amqp_message_in_dict],
        )
        response = client.get(f"/dhos/v1/amqp_message")
        assert mock_get_list.called_once
        assert response.json == [amqp_message_in_dict]

    def test_list_amqp_message_filter(
        self, mocker: MockFixture, client: FlaskClient, amqp_message_in_dict: Dict
    ) -> None:
        """Test listing AMQP messages with a filter"""
        mock_get_list = mocker.patch.object(
            controller, "get_list", return_value=[amqp_message_in_dict]
        )
        client.get(f"/dhos/v1/amqp_message?status=new")
        assert mock_get_list.called_once
        mock_get_list.assert_called_with(status_filter="new")

    def test_list_amqp_message_bad_filter(self, client: FlaskClient) -> None:
        """Test listing AMQP messages with a bad filter"""
        response = client.get(f"/dhos/v1/amqp_message?status=oops")
        assert response.status_code == 400

    def test_get_amqp_message_by_uuid(
        self, mocker: MockFixture, client: FlaskClient, amqp_message_out_dict: Dict
    ) -> None:
        """Test getting an AMQP message"""
        mock_get_message = mocker.patch.object(
            controller, "get_message", return_value=amqp_message_out_dict
        )
        response = client.get(f"/dhos/v1/amqp_message/{amqp_message_out_dict['uuid']}")
        assert mock_get_message.called_once
        assert response.json == amqp_message_out_dict

    def test_republish_amqp_message(
        self, mocker: MockFixture, client: FlaskClient
    ) -> None:
        message_uuid: str = str(uuid.uuid4())
        mock_republish: Mock = mocker.patch.object(controller, "republish_message")
        response = client.post(
            f"/dhos/v1/amqp_message/{message_uuid}/republish",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_republish.call_count == 1
        mock_republish.assert_called_with(message_uuid=message_uuid)
        assert response.status_code == 204

    def test_republish_multiple_amqp_messages(
        self, mocker: MockFixture, client: FlaskClient
    ) -> None:
        message_uuids: List[str] = [str(uuid.uuid4()) for _ in range(3)]
        mock_republish: Mock = mocker.patch.object(
            controller, "republish_multiple_messages"
        )
        response = client.post(
            f"/dhos/v1/amqp_message/republish",
            json=message_uuids,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_republish.call_count == 1
        mock_republish.assert_called_with(message_uuids=message_uuids)
        assert response.status_code == 204
