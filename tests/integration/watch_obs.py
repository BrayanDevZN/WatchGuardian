"""
Teste de WatchObs
"""

import asyncio

from src.core.module import Settings
from src.service.logs import WatchDb, WatchLogs
from src.service.obs.manage import WatchObs


async def test_watch_obs() -> None:

    # =========================================================
    # SETTINGS
    # =========================================================

    print("\n=== SETTINGS ===")

    settings = Settings()

    settings.add_secret("url")

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

    print("\n=== CREATE TABLES ===")

    await watch_db.create_tables()

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

    # Espera logs em background
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

    # Espera logs em background
    if logs._tasks:
        await asyncio.gather(
            *logs._tasks
        )

    print("\n=== OBSERVABILITY AFTER FAILURE ===")

    result = await watch_db.observability.select()

    print(result)

    # =========================================================
    # CHECK SUCCESS
    # =========================================================

    print("\n=== CHECK SUCCESS ===")

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

        print("-" * 50)

    # =========================================================
    # RESET
    # =========================================================

    print("\n=== RESET TABLES ===")

    await watch_db.reset_tables()

    print("\n=== OBSERVABILITY AFTER RESET ===")

    result = await watch_db.observability.select()

    print(result)

    # =========================================================
    # DROP TABLES
    # =========================================================

    print("\n=== DROP TABLES ===")

    await watch_db.drop_tables()

    print("\n=== TESTE FINALIZADO ===")


if __name__ == "__main__":
    asyncio.run(test_watch_obs())