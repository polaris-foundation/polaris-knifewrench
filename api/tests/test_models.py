from dhos_knifewrench_api.models import AmqpMessage


class TestModels:
    def test_model_dict(self, amqp_message_model: AmqpMessage) -> None:
        expected = {
            "routing_key": "test.123",
            "created": None,
            "created_by": None,
            "message_headers": None,
            "modified": None,
            "modified_by": None,
            "status": None,
            "uuid": None,
        }

        assert expected == amqp_message_model.to_dict_no_body()
