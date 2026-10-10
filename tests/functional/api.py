"""Teste funcional da API usando um servidor já iniciado."""

import asyncio

from src.service.module import ClientHttp, Settings, WatchAuth


ENV_FILE = ".env"


async def test_api() -> None:
    settings = Settings(env_file=ENV_FILE)

    settings.add_secret("secret")
    settings.required_secrets("secret")

    auth = WatchAuth(settings=settings)

    payload = {
        "sub": "functional-test"
    }

    user_token = await auth.user_token(payload=payload)
    refresh_token = await auth.refresh_token(payload=payload)

    client = ClientHttp(settings=settings)

    # =========================================================
    # AUTH
    # =========================================================
    print("\n=== AUTH REFRESH ===")

    auth_result = await client.auth(
        user_token=user_token,
        refresh_token=refresh_token,
    ).refresh()

    assert auth_result is not None
    assert "token" in auth_result

    user_token = auth_result["token"]

    # =========================================================
    # LOGS
    # =========================================================
    print("\n=== LOGS CREATE ===")

    logs = client.logs(token=user_token)

    log_created = await logs.create_log(
        status="INFO",
        log="functional api test",
    )

    assert log_created is not None
    assert "id" in log_created
    assert "public_id" in log_created

    log_id = log_created["id"]
    log_public_id = log_created["public_id"]

    print("\n=== LOGS GET BY ID ===")
    log_by_id = await logs.get_log(id=log_id)
    assert log_by_id is not None

    print("\n=== LOGS GET BY PUBLIC ID ===")
    log_by_public_id = await logs.get_log(public_id=log_public_id)
    assert log_by_public_id is not None

    print("\n=== LOGS GET ALL ===")
    logs_all = await logs.get_log()
    assert logs_all is not None

    print("\n=== LOGS UPDATE ===")
    log_updated = await logs.update_log(
        id=log_id,
        log="functional api test updated",
        status="SUCCESS",
    )
    assert log_updated is not None

    print("\n=== LOGS DELETE ===")
    log_deleted = await logs.delete_log(id=log_id)
    assert log_deleted is not None

    # =========================================================
    # OBSERVABILITY
    # =========================================================
    print("\n=== OBS CREATE ===")

    obs = client.obs(token=user_token)

    obs_created = await obs.create_obs(
        task="functional_api",
        status="pending",
        content="functional api test",
        latency=1,
    )

    assert obs_created is not None
    assert "id" in obs_created
    assert "public_id" in obs_created

    obs_id = obs_created["id"]
    obs_public_id = obs_created["public_id"]

    print("\n=== OBS GET BY ID ===")
    obs_by_id = await obs.get_obs(id=obs_id)
    assert obs_by_id is not None

    print("\n=== OBS GET BY PUBLIC ID ===")
    obs_by_public_id = await obs.get_obs(public_id=obs_public_id)
    assert obs_by_public_id is not None

    print("\n=== OBS GET ALL ===")
    obs_all = await obs.get_obs()
    assert obs_all is not None

    print("\n=== OBS UPDATE ===")
    obs_updated = await obs.update_obs(
        id=obs_id,
        task="functional_api_updated",
        status="sucess",
        content="functional api test finished",
        latency=2,
    )
    assert obs_updated is not None

    print("\n=== OBS DELETE ===")
    obs_deleted = await obs.delete_obs(id=obs_id)
    assert obs_deleted is not None

    print("\n=== TESTE FUNCIONAL FINALIZADO ===")


if __name__ == "__main__":
    asyncio.run(test_api())
