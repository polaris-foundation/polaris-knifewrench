from behave.runner import Context
from environs import Env
from kombu import Connection, Exchange, Message, Producer, Queue
from kombu.simple import SimpleQueue


def create_rabbitmq_infrastructure(context: Context) -> None:
    env = Env()
    host: str = env.str("RABBITMQ_HOST")
    port: int = env.int("RABBITMQ_PORT", 5672)
    username: str = env.str("RABBITMQ_USERNAME")
    password: str = env.str("RABBITMQ_PASSWORD")

    # Create rabbit connection
    conn_string: str = f"amqp://{username}:{password}@{host}:{port}//"
    connection: Connection = Connection(conn_string)

    # Declare dead letter exchange and queue
    dlx_exchange = Exchange("dhos-dlx", "fanout")
    error_queue = Queue(
        "errors", exchange=dlx_exchange, routing_key="errors", channel=connection
    )
    error_queue.declare()

    # Declare normal exchange, linked to DLX, and test queue which will deadletter
    exchange = Exchange("dhos", "topic")
    test_queue = Queue(
        "test_queue",
        exchange=exchange,
        routing_key="dhos.123",
        queue_arguments={"x-dead-letter-exchange": "dhos-dlx"},
        message_ttl=1,
        channel=connection,
    )
    test_queue.declare()
    destination_queue = Queue(
        "destination_queue",
        exchange=exchange,
        routing_key="dhos.999",
        queue_arguments={"x-dead-letter-exchange": "dhos-dlx"},
        channel=connection,
    )
    destination_queue.declare()
    context.rabbit_connection = connection
    context.rabbit_exchange = exchange
    context.test_queue = test_queue
    context.destination_queue = destination_queue


def publish_message(
    connection: Connection,
    exchange: Exchange,
    routing_key: str,
    body: str,
    message_identifier: str,
) -> None:
    with connection as conn:
        producer: Producer = conn.Producer(serializer="json")
        producer.publish(
            body,
            headers={"x-message-identifier": message_identifier},
            exchange=exchange,
            routing_key=routing_key,
            message_ttl=1,
            retry=True,
            retry_policy={
                "interval_start": 1,
                "interval_step": 1,
                "interval_max": 5,
                "max_retries": 10,
            },
        )


def get_message_on_queue(queue: Queue, context: Context) -> Message:
    simple_queue: SimpleQueue = SimpleQueue(context.rabbit_connection, queue)
    message: Message = simple_queue.get(block=True, timeout=10)
    message.ack()
    return message
