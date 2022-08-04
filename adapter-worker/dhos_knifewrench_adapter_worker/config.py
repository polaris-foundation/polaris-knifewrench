from typing import Optional

from environs import Env


class Config:
    RABBITMQ_CONNECTION_STRING: Optional[str] = None
    DHOS_KNIFEWRENCH_API: Optional[str] = None

    def __init__(self) -> None:
        env: Env = Env()
        rabbitmq_host: str = env.str("RABBITMQ_HOST")
        rabbitmq_port: int = env.int("RABBITMQ_PORT", default=5672)
        rabbitmq_username: str = env.str("RABBITMQ_USERNAME")
        rabbitmq_password: str = env.str("RABBITMQ_PASSWORD")
        self.RABBITMQ_CONNECTION_STRING: str = f"amqp://{rabbitmq_username}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}//"
        self.DHOS_KNIFEWRENCH_API: str = env.str("DHOS_KNIFEWRENCH_API_HOST")
