"""
Teste de db.
"""

import asyncio

from WatchGuardian._internal.database.manage import ControlDb
from WatchGuardian._internal.core.module import config_url


async def test_db() -> None:

    url = config_url()

    control_db = ControlDb(
        url=url
    )

    await control_db.run()

    print("\n=== CREATE LOG ===")

    log_created = await control_db.logs.create(
        log="Teste de criação de log",
        status="INFO"
    )

    print(log_created)

    log_id = log_created["id"]
    log_public_id = log_created["public_id"]

    print("\n=== SELECT LOG BY ID ===")
    print(await control_db.logs.select(id=log_id))

    print("\n=== SELECT LOG BY PUBLIC ID ===")
    print(await control_db.logs.select(public_id=log_public_id))

    print("\n=== SELECT ALL LOGS ===")
    print(await control_db.logs.select())

    print("\n=== UPDATE LOG ===")
    result = await control_db.logs.update(
        id=log_id,
        log="Log atualizado com sucesso",
        status="SUCCESS"
    )
    print(result)
    assert result["memory_bytes"] == 1024

    print("\n=== SELECT LOG UPDATED ===")
    print(await control_db.logs.select(id=log_id))

    print("\n=== CREATE OBSERVABILITY ===")

    observability_created = await control_db.observability.create(
        group="unit_tests",
        task="test_task",
        status="pending",
        content="Processando tarefa de teste",
        latency=0,
        memory_bytes=0,
    )

    print(observability_created)
    assert observability_created["memory_bytes"] == 0

    observability_id = observability_created["id"]
    observability_public_id = observability_created["public_id"]

    print("\n=== SELECT OBSERVABILITY BY ID ===")
    print(await control_db.observability.select(id=observability_id))

    print("\n=== SELECT OBSERVABILITY BY PUBLIC ID ===")
    print(await control_db.observability.select(public_id=observability_public_id))

    print("\n=== SELECT ALL OBSERVABILITY ===")
    print(await control_db.observability.select())

    print("\n=== UPDATE OBSERVABILITY TO SUCCESS ===")
    result = await control_db.observability.update(
        id=observability_id,
        group="unit_tests_updated",
        status="success",
        content="Processamento finalizado",
        memory_bytes=1024,
    )
    print(result)

    print("\n=== SELECT OBSERVABILITY UPDATED ===")
    print(await control_db.observability.select(id=observability_id))

    print("\n=== CREATE DATA FOR RESET TEST ===")

    await control_db.logs.create(
        log="Esse log será apagado pelo reset",
        status="WARNING"
    )

    await control_db.observability.create(
        group="reset_tests",
        task="reset_test",
        status="pending",
        content="Essa operação será apagada pelo reset",
        latency=0,
        memory_bytes=0,
    )

    print("\nLogs antes do reset:")
    print(await control_db.logs.select())

    print("\nObservability antes do reset:")
    print(await control_db.observability.select())

    print("\n=== RESET TABLES ===")
    await control_db.reset_tables()

    print("\nLogs depois do reset:")
    print(await control_db.logs.select())

    print("\nObservability depois do reset:")
    print(await control_db.observability.select())

    print("\n=== TESTE FINALIZADO ===")


if __name__ == "__main__":
    asyncio.run(test_db())
