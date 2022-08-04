import json
import time
from json import JSONDecodeError
from typing import Any, AnyStr, Dict, List, Optional

import requests
from kombu import Connection, Message, Queue
from kombu.mixins import ConsumerMixin
from she_logging import logger

import dhos_knifewrench_adapter_worker.config
from dhos_knifewrench_adapter_worker.auth_token import get_api_jwt


class ErrorQueueConsumer(ConsumerMixin):
    def __init__(self, connection: Connection, queues: List[Queue]) -> None:
        self.connection = connection
        self.queues = queues
        self.config = dhos_knifewrench_adapter_worker.config.Config()

    def get_consumers(self, consumer: Any, _: Any) -> List[ConsumerMixin]:
        return [consumer(self.queues, callbacks=[self.on_message], accept=["json"])]

    def on_message(self, body: AnyStr, message: Message) -> None:
        """Callback for error messages."""
        # noinspection PyBroadException
        try:
            self._process_message(body, message)
        except Exception:
            logger.exception("Exception while processing message")
            message.requeue()

    def _process_message(self, body: AnyStr, message: Message) -> None:
        logger.info("Removed error message from error queue")

        amqp_body: Optional[Dict] = None
        try:
            amqp_body = json.loads(message.payload)
        except JSONDecodeError:
            logger.info("Couldn't decode message body as JSON")

        try:
            latest_delivery_attempt = message.headers["x-death"][0]
            original_routing_key = latest_delivery_attempt["routing-keys"][0]
        except (KeyError, TypeError):
            logger.info("Couldn't get routing key from message headers")
            original_routing_key = None

        payload: Dict[str, Any] = {
            "routing_key": original_routing_key,
            "body": amqp_body,
            "headers": message.headers,
            "raw_body": str(message.payload),
        }

        logger.debug("Posting message to knifewrench API", extra={"payload": payload})
        try:
            res: requests.Response = requests.post(
                f"{self.config.DHOS_KNIFEWRENCH_API}/dhos/v1/amqp_message",
                data=json.dumps(payload, sort_keys=True, default=str),
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {get_api_jwt()}",
                    "Content-Type": "application/json",
                },
            )
            res.raise_for_status()
        except requests.exceptions.RequestException:
            # Couldn't process the message, so NACK it. This is unlikely to happen, but if it does then knifewrench
            # will immediately try to process the message again - so add a delay to prevent spamming the API.
            logger.exception(
                "Could not send error message to knifewrench API - requeuing to error queue"
            )
            time.sleep(10)
            message.requeue()
            return

        # Successfully processed the message, so ACK it.
        message.ack()
        logger.info("Successfully sent error message to knifewrench API")
