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
    print(logs_without_db.debug("Teste debug sem banco"))

    print("\n=== INFO ===")
    print(logs_without_db.info("Teste info sem banco"))

    print("\n=== SUCCESS ===")
    print(logs_without_db.success("Teste success sem banco"))

    print("\n=== WARNING ===")
    print(logs_without_db.warning("Teste warning sem banco"))

    print("\n=== ERROR ===")
    print(logs_without_db.error("Teste error sem banco"))

    print("\n=== CRITICAL ===")
    print(logs_without_db.critical("Teste critical sem banco"))

    # =========================================================
    # WATCHDB
    # =========================================================

    print("\n=== CREATE WATCHDB ===")

    watch_db = await WatchDb(
        settings=settings
    )

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
    print(logs.debug("Teste debug com banco"))

    print("\n=== INFO ===")
    print(logs.info("Teste info com banco"))

    print("\n=== SUCCESS ===")
    print(logs.success("Teste success com banco"))

    print("\n=== WARNING ===")
    print(logs.warning("Teste warning com banco"))

    print("\n=== ERROR ===")
    print(logs.error("Teste error com banco"))

    print("\n=== CRITICAL ===")
    print(logs.critical("Teste critical com banco"))

    # =========================================================
    # ESPERA BACKGROUND TASKS
    # =========================================================

    print("\n=== WAIT BACKGROUND TASKS ===")

    if logs._tasks:
        await asyncio.gather(*logs._tasks)

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
    print(
        warning_logs.debug(
            "Esse debug não deveria aparecer"
        )
    )

    print("\nINFO SHOULD NOT RUN:")
    print(
        warning_logs.info(
            "Esse info não deveria aparecer"
        )
    )

    print("\nSUCCESS SHOULD NOT RUN:")
    print(
        warning_logs.success(
            "Esse success não deveria aparecer"
        )
    )

    print("\nWARNING SHOULD RUN:")
    print(
        warning_logs.warning(
            "Esse warning deve aparecer"
        )
    )

    print("\nERROR SHOULD RUN:")
    print(
        warning_logs.error(
            "Esse error deve aparecer"
        )
    )

    print("\nCRITICAL SHOULD RUN:")
    print(
        warning_logs.critical(
            "Esse critical deve aparecer"
        )
    )

    if warning_logs._tasks:
        await asyncio.gather(*warning_logs._tasks)

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