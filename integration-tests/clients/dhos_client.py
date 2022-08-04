from datetime import datetime, timedelta
from typing import Dict

import requests
from environs import Env
from jose import jwt as jose_jwt
from requests import Response


def get_system_token() -> str:
    system_jwt = jose_jwt.encode(
        claims={
            "metadata": {"system_id": "dhos-robot"},
            "iss": "http://localhost/",
            "aud": "http://localhost/",
            "scope": Env().str("SYSTEM_JWT_SCOPE"),
            "exp": datetime.utcnow() + timedelta(seconds=300),
        },
        key=Env().str("HS_KEY"),
        algorithm="HS512",
    )
    return system_jwt


def create_amqp_message(message_details: Dict, jwt: str) -> Response:
    response = requests.post(
        url="http://dhos-knifewrench-api:5000/dhos/v1/amqp_message",
        headers={"Authorization": f"Bearer {jwt}"},
        json=message_details,
        timeout=15,
    )
    response.raise_for_status()
    return response


def get_all_amqp_messages(jwt: str) -> Response:
    response = requests.get(
        url="http://dhos-knifewrench-api:5000/dhos/v1/amqp_message",
        headers={"Authorization": f"Bearer {jwt}"},
        timeout=15,
    )
    response.raise_for_status()
    return response


def get_amqp_message(uuid: str, jwt: str) -> Response:
    response = requests.get(
        url=f"http://dhos-knifewrench-api:5000/dhos/v1/amqp_message/{uuid}",
        headers={"Authorization": f"Bearer {jwt}"},
        timeout=15,
    )
    response.raise_for_status()
    return response


def republish_amqp_message(uuid: str, jwt: str) -> Response:
    response = requests.post(
        url=f"http://dhos-knifewrench-api:5000/dhos/v1/amqp_message/{uuid}/republish",
        headers={"Authorization": f"Bearer {jwt}"},
        timeout=15,
    )
    response.raise_for_status()
    return response
