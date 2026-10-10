"""
Teste de WatchObs
"""

import asyncio

from src.service.module import Settings, WatchDb, WatchLogs, WatchObs


async def test_watch_obs() -> None:

    # =========================================================
    # SETTINGS
    # =========================================================

    print("\n=== SETTINGS ===")

    settings = Settings()

    settings.add_secret("url_db")

    settings.add_config({
        "name": "path",
        "value": None
    })

    # =========================================================
    # WATCHDB
    # =========================================================

    print("\n=== CREATE WATCHDB ===")

    watch_db = await WatchDb(
        settings=settings
    )

    print("\n=== RESET TABLES ===")

    await watch_db.reset_tables()

    # =========================================================
    # WATCHLOGS
    # =========================================================

    print("\n=== CREATE WATCHLOGS ===")

    logs = WatchLogs(
        loglevel="DEBUG",
        watch_db=watch_db
    )

    # =========================================================
    # WATCHOBS
    # =========================================================

    print("\n=== CREATE WATCHOBS ===")

    watch_obs = WatchObs(
        logs=logs,
        watch_db=watch_db
    )

    # =========================================================
    # SUCCESS TASK
    # =========================================================

    print("\n=== SUCCESS TASK ===")

    async with watch_obs.begin("success_task"):
        print("Executando task de sucesso...")

        await asyncio.sleep(1)

        print("Task finalizada normalmente")

    if logs._tasks:
        await asyncio.gather(
            *logs._tasks
        )

    print("\n=== OBSERVABILITY AFTER SUCCESS ===")

    result = await watch_db.observability.select()

    print(result)

    # =========================================================
    # FAILURE TASK
    # =========================================================

    print("\n=== FAILURE TASK ===")

    try:

        async with watch_obs.begin("failure_task"):
            print("Executando task que vai falhar...")

            await asyncio.sleep(1)

            raise ValueError(
                "Erro de teste do WatchObs"
            )

    except ValueError as error:

        print(
            f"Erro capturado fora do context manager: {error}"
        )

    if logs._tasks:
        await asyncio.gather(
            *logs._tasks
        )

    print("\n=== OBSERVABILITY AFTER FAILURE ===")

    result = await watch_db.observability.select()

    print(result)

    # =========================================================
    # CHECK RESULTS
    # =========================================================

    print("\n=== CHECK RESULTS ===")

    data = await watch_db.observability.select()

    for item in data:

        print(
            "TASK:",
            item.get("task")
        )

        print(
            "STATUS:",
            item.get("status")
        )

        print(
            "CONTENT:",
            item.get("content")
        )

        print(
            "LATENCY:",
            item.get("latency")
        )

        print(
            "CREATED_AT:",
            item.get("created_at")
        )

        print(
            "UPDATE_AT:",
            item.get("update_at")
        )

        print("-" * 50)

    # =========================================================
    # RESET
    # =========================================================

    print("\n=== RESET TABLES ===")

    await watch_db.reset_tables()

    print("\n=== OBSERVABILITY AFTER RESET ===")

    result = await watch_db.observability.select()

    print(result)

    print("\n=== TESTE FINALIZADO ===")


if __name__ == "__main__":
    asyncio.run(test_watch_obs())