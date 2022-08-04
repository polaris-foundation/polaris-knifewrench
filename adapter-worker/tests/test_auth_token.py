from jose import jwt as jose_jwt

from dhos_knifewrench_adapter_worker import auth_token


def _has_expired(jwt: str) -> bool:
    try:
        jose_jwt.decode(
            jwt,
            "dummykey",
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_iat": False,
                "verify_exp": True,
                "verify_nbf": False,
                "verify_iss": False,
                "verify_sub": False,
                "verify_jti": False,
                "verify_at_hash": False,
                "leeway": 0,
            },
        )
        return False
    except jose_jwt.ExpiredSignatureError:
        return True


class TestAuthToken:
    def test_get_api_jwt(self) -> None:
        first_result = auth_token.get_api_jwt()
        assert not _has_expired(first_result)
