"""Executa a CLI real para testes funcionais."""

import os
from datetime import datetime, timedelta, timezone

import jwt

from src.cli.main import main


TEST_SECRET = "watchguardian-functional-test-secret-2026"


def _set_test_token() -> None:
    payload = {
        "sub": "functional-cli-test",
        "type": "user_token",
        "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
    }

    os.environ["token"] = jwt.encode(
        payload=payload,
        key=TEST_SECRET,
        algorithm="HS256",
    )


if __name__ == "__main__":
    _set_test_token()
    main()
