from typing import List

from kombu import Connection, Exchange, Queue

from .config import Config
from .knifewrench import ErrorQueueConsumer

config = Config()

_connection: Connection = Connection(config.RABBITMQ_CONNECTION_STRING)
_exchange: Exchange = Exchange("dhos-dlx", type="fanout")
_queues: List[Queue] = [Queue("errors", exchange=_exchange)]

ErrorQueueConsumer(_connection, _queues).run()
