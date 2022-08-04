from typing import Dict, List, Optional

import flask
from flask_batteries_included.helpers.security import protected_route
from flask_batteries_included.helpers.security.endpoint_security import scopes_present
from she_logging import logger

from dhos_knifewrench_api.api import controller

api_blueprint = flask.Blueprint("api", __name__)


@api_blueprint.route("/dhos/v1/amqp_message", methods=["POST"])
@protected_route(scopes_present(required_scopes="write:error_message"))
def create_amqp_message(amqp_message_details: Dict) -> flask.Response:
    """
    ---
    post:
      summary: Create AMQP message
      description: Create a record of an errored AMQP message
      tags: [message]
      requestBody:
        description: JSON body containing the AMQP message
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MessageRequest'
              x-body-name: amqp_message_details
      responses:
        '201':
          description: New AMQP message created
          headers:
            Location:
              description: The location of the created AMQP message
              schema:
                type: string
                example: http://localhost/dhos/v1/patient/2c4f1d24-2952-4d4e-b1d1-3637e33cc161
        default:
          description: >-
              Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    logger.debug("Create AMQP message route hit")
    amqp_message: Dict = controller.create(amqp_message_details)
    response = flask.make_response("", 201)
    response.headers["Location"] = f"/dhos/v1/patient/{amqp_message['uuid']}"
    return response


# Not protected as the UI requires access.
@api_blueprint.route("/dhos/v1/amqp_message", methods=["GET"])
def get_amqp_message_list(status: Optional[str] = None) -> flask.Response:
    """
    ---
    get:
      summary: Get all AMQP messages
      description: Get a list of errored AMQP messages
      tags: [message]
      parameters:
        - name: status
          in: query
          required: false
          description: Status filter
          schema:
            type: string
            enum: ["new", "archived", "republished"]
            example: new
      responses:
        '200':
          description: List of AMQP message
          content:
            application/json:
              schema:
                type: array
                items: MessageResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    logger.debug("Get all AMQP messages route hit")
    amqp_messages: List[Dict] = controller.get_list(status_filter=status)
    return flask.jsonify(amqp_messages)


# Not protected as the UI requires access.
@api_blueprint.route("/dhos/v1/amqp_message/<message_uuid>", methods=["GET"])
def get_amqp_message(message_uuid: str) -> flask.Response:
    """
    ---
    get:
      summary: Get AMQP message
      description: Get an errored AMQP message by UUID
      tags: [message]
      parameters:
        - name: message_uuid
          in: path
          required: true
          description: The AMQP message UUID
          schema:
            type: string
            example: '18439f36-ffa9-42ae-90de-0beda299cd37'
      responses:
        '200':
          description: The AMQP message
          content:
            application/json:
              schema: MessageResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    logger.debug("Get AMQP message route hit")
    return flask.jsonify(controller.get_message(message_uuid=message_uuid))


@api_blueprint.route("/dhos/v1/amqp_message/<message_uuid>/republish", methods=["POST"])
@protected_route(scopes_present(required_scopes="write:error_message"))
def republish_amqp_message(message_uuid: str) -> flask.Response:
    """
    ---
    post:
      summary: Republish AMQP message
      description: >-
        Republish an errored AMQP message by UUID using its routing key. Responds with a 204 on
        successful republish.
      tags: [message]
      parameters:
        - name: message_uuid
          in: path
          required: true
          description: The AMQP message UUID
          schema:
            type: string
            example: '18439f36-ffa9-42ae-90de-0beda299cd37'
      responses:
        '204':
          description: AMQP message successfully republished
        default:
          description: >-
              Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    logger.debug("Republish AMQP message route hit")
    controller.republish_message(message_uuid=message_uuid)
    return flask.make_response("", 204)


@api_blueprint.route("/dhos/v1/amqp_message/republish", methods=["POST"])
@protected_route(scopes_present(required_scopes="write:error_message"))
def republish_multiple_amqp_message(message_uuids: List[str]) -> flask.Response:
    """
    ---
    post:
      summary: Republish multiple AMQP messages
      description: >-
        Republish multiple errored AMQP message using its routing key. Responds with a 204 on
        successful republish of all messages.
      tags: [message]
      requestBody:
        description: List of AMQP message UUIDs
        required: true
        content:
          application/json:
            schema:
              type: array
              items:
                type: string
                example: 18439f36-ffa9-42ae-90de-0beda299cd37
              x-body-name: message_uuids
      responses:
        '204':
          description: AMQP messages successfully republished
        default:
          description: >-
              Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    logger.debug("Republish multiple AMQP messages route hit")
    controller.republish_multiple_messages(message_uuids=message_uuids)
    return flask.make_response("", 204)
