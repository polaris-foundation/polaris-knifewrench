import os
from datetime import datetime, timedelta

from jose import jwt as jose_jwt

HS_KEY: str = os.environ["HS_KEY"]
PROXY_URL: str = os.environ["PROXY_URL"].rstrip("/") + "/"
HS_ISSUER: str = PROXY_URL
JWT_EXPIRY_IN_SECONDS: int = int(os.environ.get("JWT_EXPIRY_IN_SECONDS", 86400))


def get_api_jwt() -> str:
    metadata = {"can_edit_ews": True, "system_id": "dhos-robot"}
    return jose_jwt.encode(
        {
            "metadata": metadata,
            "iss": HS_ISSUER,
            "aud": PROXY_URL,
            "scope": "write:error_message",
            "exp": datetime.utcnow() + timedelta(seconds=JWT_EXPIRY_IN_SECONDS),
        },
        key=HS_KEY,
        algorithm="HS512",
    )
