"""
Teste de WatchAuth.
"""

import asyncio
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

    payload = {
        "sub": "test-user",
        "role": "admin"
    }

    print("\n=== ENCODE ===")

    token = await watch_auth.encode(
        payload=payload
    )

    print(token)

    print("\n=== DECODE ===")

    decoded = await watch_auth.decode(
        token=token
    )

    print(decoded)

    assert decoded == payload

    print("\n=== TESTE FINALIZADO ===")


if __name__ == "__main__":
    asyncio.run(test_token())
