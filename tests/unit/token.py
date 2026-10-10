"""
Teste de WatchAuth.
"""

import asyncio
from datetime import datetime, timedelta, timezone
import os

from src.service.module import Settings, WatchAuth


async def test_token() -> None:

    print("\n=== SECRET ===")

    watch_auth = WatchAuth()
    secret = watch_auth.secret()

    print(secret)

    print("\n=== SETTINGS ===")

    os.environ["secret"] = secret

    settings = Settings()
    settings.add_secret("secret")
    settings.required_secrets("secret")

    print("\n=== CREATE AUTH ===")

    watch_auth = WatchAuth(
        settings=settings
    )

    exp = datetime.now(timezone.utc) + timedelta(hours=1)

    print("\n=== USER TOKEN ===")

    token = await watch_auth.user_token(
        exp=exp
    )

    print(token)

    print("\n=== DECODE ===")

    decoded = await watch_auth.decode(
        token=token
    )

    print(decoded)

    assert decoded["type"] == "user_token"
    assert decoded["exp"] == int(exp.timestamp())
    assert set(decoded.keys()) == {"exp", "type"}

    print("\n=== TESTE FINALIZADO ===")


if __name__ == "__main__":
    asyncio.run(test_token())
