"""
Teste de WatchLogs
"""

import asyncio

from src.service.logs import WatchDb, WatchLogs
from src.service.db import Settings


async def test_watch_logs() -> None:

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
    # WATCHLOGS SEM BANCO
    # =========================================================

    print("\n=== WATCHLOGS WITHOUT DB ===")

    logs_without_db = WatchLogs(
        loglevel="DEBUG"
    )

    print("\n=== DEBUG ===")
    print(
        logs_without_db.debug(
            "Teste debug sem banco"
        )
    )

    print("\n=== INFO ===")
    print(
        logs_without_db.info(
            "Teste info sem banco"
        )
    )

    print("\n=== SUCCESS ===")
    print(
        logs_without_db.success(
            "Teste success sem banco"
        )
    )

    print("\n=== WARNING ===")
    print(
        logs_without_db.warning(
            "Teste warning sem banco"
        )
    )

    print("\n=== ERROR ===")
    print(
        logs_without_db.error(
            "Teste error sem banco"
        )
    )

    print("\n=== CRITICAL ===")
    print(
        logs_without_db.critical(
            "Teste critical sem banco"
        )
    )

    # =========================================================
    # WATCHDB
    # =========================================================

    print("\n=== CREATE WATCHDB ===")

    watch_db = await WatchDb(
        settings=settings
    )

    # Limpa dados antigos antes do teste
    await watch_db.reset_tables()

    # =========================================================
    # WATCHLOGS COM BANCO
    # =========================================================

    print("\n=== WATCHLOGS WITH DB ===")

    logs = WatchLogs(
        loglevel="DEBUG",
        watch_db=watch_db
    )

    print("\n=== DEBUG ===")

    result = logs.debug(
        "Teste debug com banco"
    )

    print(result)

    print("\n=== INFO ===")

    result = logs.info(
        "Teste info com banco"
    )

    print(result)

    print("\n=== SUCCESS ===")

    result = logs.success(
        "Teste success com banco"
    )

    print(result)

    print("\n=== WARNING ===")

    result = logs.warning(
        "Teste warning com banco"
    )

    print(result)

    print("\n=== ERROR ===")

    result = logs.error(
        "Teste error com banco"
    )

    print(result)

    print("\n=== CRITICAL ===")

    result = logs.critical(
        "Teste critical com banco"
    )

    print(result)

    # =========================================================
    # ESPERA BACKGROUND TASKS
    # =========================================================

    print("\n=== WAIT BACKGROUND TASKS ===")

    if logs._tasks:
        await asyncio.gather(
            *logs._tasks
        )

    # =========================================================
    # SELECT LOGS
    # =========================================================

    print("\n=== SELECT ALL LOGS ===")

    result = await watch_db.logs.select()

    print(result)

    # =========================================================
    # TESTE DE LOGLEVEL
    # =========================================================

    print("\n=== TEST LOGLEVEL WARNING ===")

    warning_logs = WatchLogs(
        loglevel="WARNING",
        watch_db=watch_db
    )

    print("\nDEBUG SHOULD NOT RUN:")

    result = warning_logs.debug(
        "Esse debug não deveria aparecer"
    )

    print(result)

    print("\nINFO SHOULD NOT RUN:")

    result = warning_logs.info(
        "Esse info não deveria aparecer"
    )

    print(result)

    print("\nWARNING SHOULD RUN:")

    result = warning_logs.warning(
        "Esse warning deve aparecer"
    )

    print(result)

    print("\nERROR SHOULD RUN:")

    result = warning_logs.error(
        "Esse error deve aparecer"
    )

    print(result)

    if warning_logs._tasks:
        await asyncio.gather(
            *warning_logs._tasks
        )

    # =========================================================
    # SELECT AFTER LOGLEVEL
    # =========================================================

    print("\n=== LOGS AFTER LOGLEVEL TEST ===")

    result = await watch_db.logs.select()

    print(result)

    # =========================================================
    # RESET
    # =========================================================

    print("\n=== RESET TABLES ===")

    await watch_db.reset_tables()

    print("\n=== LOGS AFTER RESET ===")

    result = await watch_db.logs.select()

    print(result)

    print("\n=== TESTE FINALIZADO ===")


if __name__ == "__main__":
    asyncio.run(test_watch_logs())