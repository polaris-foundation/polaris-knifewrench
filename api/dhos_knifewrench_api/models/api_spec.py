from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_batteries_included.helpers.apispec import (
    FlaskBatteriesPlugin,
    Identifier,
    initialise_apispec,
    openapi_schema,
)
from marshmallow import EXCLUDE, Schema, fields
from marshmallow.validate import OneOf

dhos_knifewrench_api_spec: APISpec = APISpec(
    version="1.0.0",
    openapi_version="3.0.3",
    title="DHOS Knifewrench API",
    info={
        "description": "The DHOS Knifewrench API is responsible for storing and retrieving errored AMQP messages."
    },
    plugins=[FlaskPlugin(), MarshmallowPlugin(), FlaskBatteriesPlugin()],
)

initialise_apispec(dhos_knifewrench_api_spec)

HEADERS_EXAMPLE = {
    "x-first-death-queue": "dhos-rules-adapter-task-queue",
    "x-first-death-reason": "rejected",
    "x-first-death-exchange": "dhos",
    "x-death": [
        {
            "time": "2019-01-14 12:52:47",
            "count": 1,
            "queue": "dhos-rules-adapter-task-queue",
            "reason": "rejected",
            "exchange": "dhos",
            "routing-keys": ["send.1102421000000108"],
        }
    ],
}


@openapi_schema(dhos_knifewrench_api_spec)
class MessageRequest(Schema):
    class Meta:
        title = "Message request"
        unknown = EXCLUDE
        ordered = True

    routing_key = fields.String(
        required=True,
        allow_none=True,
        example="gdm.12345",
        description="The AMQP routing key used to originally route this message",
    )
    headers = fields.Raw(
        required=False,
        nullable=True,
        example=HEADERS_EXAMPLE,
        description="AMQP message headers",
    )
    body = fields.Raw(
        required=False,
        nullable=True,
        example={"key": "value"},
        description="JSON body of the message, or null if the body could not be loaded as JSON",
    )
    raw_body = fields.String(
        required=True,
        example="some body once told me the world was gonna roll me",
        description="Raw message body bytes",
    )


@openapi_schema(dhos_knifewrench_api_spec)
class MessageResponse(Identifier):
    class Meta:
        title = "Message response"
        unknown = EXCLUDE
        ordered = True

    message_headers = (
        fields.Dict(
            required=False, description="AMQP message headers", example=HEADERS_EXAMPLE
        ),
    )
    message_body = fields.Raw(
        required=False,
        description="JSON body of the message, or null if the body could not be loaded as JSON",
        example={"key": "value"},
    )
    routing_key = fields.String(
        required=True,
        allow_none=True,
        example="gdm.12345",
        description="The AMQP routing key used to originally route this message",
    )
    status = fields.String(
        required=True,
        decription="Message status",
        validate=OneOf(["new", "archived", "republished"]),
    )
