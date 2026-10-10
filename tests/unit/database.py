"""
Teste de db.
"""

import asyncio

from src.database.manage import ControlDb
from src.core.module import config_url


async def test_db() -> None:

    url = config_url()

    control_db = ControlDb(
        url=url
    )

    await control_db.run()

    # =========================================================
    # LOGS
    # =========================================================

    print("\n=== CREATE LOG ===")

    log_created = await control_db.logs.create(
        log="Teste de criação de log",
        status="INFO"
    )

    print(log_created)

    log_id = log_created["id"]
    log_public_id = log_created["public_id"]

    print("\n=== SELECT LOG BY ID ===")

    result = await control_db.logs.select(
        id=log_id
    )

    print(result)

    print("\n=== SELECT LOG BY PUBLIC ID ===")

    result = await control_db.logs.select(
        public_id=log_public_id
    )

    print(result)

    print("\n=== SELECT ALL LOGS ===")

    result = await control_db.logs.select()

    print(result)

    print("\n=== UPDATE LOG ===")

    result = await control_db.logs.update(
        id=log_id,
        log="Log atualizado com sucesso",
        status="SUCCESS"
    )

    print(result)

    print("\n=== SELECT LOG UPDATED ===")

    result = await control_db.logs.select(
        id=log_id
    )

    print(result)

    # =========================================================
    # OBSERVABILITY
    # =========================================================

    print("\n=== CREATE OBSERVABILITY ===")

    observability_created = await control_db.observability.create(
        task="test_task",
        status="pending",
        content="Processando tarefa de teste",
        latency=0
    )

    print(observability_created)

    observability_id = observability_created["id"]
    observability_public_id = observability_created["public_id"]

    print("\n=== SELECT OBSERVABILITY BY ID ===")

    result = await control_db.observability.select(
        id=observability_id
    )

    print(result)

    print("\n=== SELECT OBSERVABILITY BY PUBLIC ID ===")

    result = await control_db.observability.select(
        public_id=observability_public_id
    )

    print(result)

    print("\n=== SELECT ALL OBSERVABILITY ===")

    result = await control_db.observability.select()

    print(result)

    print("\n=== UPDATE OBSERVABILITY TO SUCCESS ===")

    result = await control_db.observability.update(
        id=observability_id,
        status="success",
        content="Processamento finalizado"
    )

    print(result)

    print("\n=== SELECT OBSERVABILITY UPDATED ===")

    result = await control_db.observability.select(
        id=observability_id
    )

    print(result)

    # =========================================================
    # RESET TABLES
    # =========================================================

    print("\n=== CREATE DATA FOR RESET TEST ===")

    await control_db.logs.create(
        log="Esse log será apagado pelo reset",
        status="WARNING"
    )

    await control_db.observability.create(
        task="reset_test",
        status="pending",
        content="Essa operação será apagada pelo reset",
        latency=0
    )

    print("\nLogs antes do reset:")

    print(
        await control_db.logs.select()
    )

    print("\nObservability antes do reset:")

    print(
        await control_db.observability.select()
    )

    print("\n=== RESET TABLES ===")

    await control_db.reset_tables()

    print("\nLogs depois do reset:")

    print(
        await control_db.logs.select()
    )

    print("\nObservability depois do reset:")

    print(
        await control_db.observability.select()
    )

    print("\n=== TESTE FINALIZADO ===")


if __name__ == "__main__":
    asyncio.run(test_db())