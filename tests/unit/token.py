"""
Teste de WatchAuth.
"""

import asyncio
from datetime import datetime, timezone
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

    print("\n=== USER TOKEN ===")

    before = datetime.now(timezone.utc).timestamp()
    token = await watch_auth.user_token()
    after = datetime.now(timezone.utc).timestamp()

    print(token)

    print("\n=== DECODE USER TOKEN ===")

    decoded = await watch_auth.decode(
        token=token
    )

    print(decoded)

    assert decoded["type"] == "user_token"
    assert before + 3600 <= decoded["exp"] <= after + 3600
    assert set(decoded.keys()) == {"exp", "type"}

    print("\n=== REFRESH TOKEN ===")

    refresh_token = await watch_auth.refresh_token()

    print(refresh_token)

    print("\n=== DECODE REFRESH TOKEN ===")

    decoded_refresh = await watch_auth.decode(
        token=refresh_token
    )

    print(decoded_refresh)

    assert decoded_refresh == {
        "type": "refresh_token"
    }

    print("\n=== TESTE FINALIZADO ===")


if __name__ == "__main__":
    asyncio.run(test_token())
