"""
Teste de WatchObs
"""

import asyncio

from src.service.module import Settings, WatchDb, WatchLogs, WatchObs


async def test_watch_obs() -> None:

    print("\n=== SETTINGS ===")

    settings = Settings()
    settings.add_secret("url_db")
    settings.add_config({
        "name": "path",
        "value": None
    })

    print("\n=== CREATE WATCHDB ===")

    watch_db = await WatchDb(settings=settings)

    await watch_db.create_tables()

    print("\n=== RESET TABLES ===")
    await watch_db.reset_tables()

    print("\n=== CREATE WATCHLOGS ===")

    logs = WatchLogs(
        loglevel="DEBUG",
        watch_db=watch_db
    )

    print("\n=== CREATE WATCHOBS ===")

    watch_obs = WatchObs(
        logs=logs,
        watch_db=watch_db
    )

    print("\n=== SUCCESS TASK ===")

    async with watch_obs.begin("success_task", group="integration_tests") as task_context:
        pending = await watch_db.observability.select(public_id=task_context.id)
        assert pending["memory_bytes"] == task_context._memory_start
        print("Executando task de sucesso...")
        await asyncio.sleep(1)
        print("Task finalizada normalmente")

    completed = await watch_db.observability.select(public_id=task_context.id)
    assert completed["status"] == "success"
    assert isinstance(completed["memory_bytes"], int)
    assert completed["memory_bytes"] >= 0

    if logs._tasks:
        await asyncio.gather(*logs._tasks)

    print("\n=== OBSERVABILITY AFTER SUCCESS ===")
    print(await watch_db.observability.select())

    print("\n=== FAILURE TASK ===")

    try:
        async with watch_obs.begin("failure_task", group="integration_tests") as failed_context:
            pending = await watch_db.observability.select(public_id=failed_context.id)
            assert pending["memory_bytes"] == failed_context._memory_start
            print("Executando task que vai falhar...")
            await asyncio.sleep(1)
            raise ValueError("Erro de teste do WatchObs")

    except ValueError as error:
        print(f"Erro capturado fora do context manager: {error}")

    failed = await watch_db.observability.select(public_id=failed_context.id)
    assert failed["status"] == "failure"
    assert isinstance(failed["memory_bytes"], int)
    assert failed["memory_bytes"] >= 0

    if logs._tasks:
        await asyncio.gather(*logs._tasks)

    print("\n=== OBSERVABILITY AFTER FAILURE ===")
    print(await watch_db.observability.select())

    print("\n=== CHECK RESULTS ===")

    data = await watch_db.observability.select()
    assert all(isinstance(item.get("memory_bytes"), int) for item in data)
    assert all(item["memory_bytes"] >= 0 for item in data)

    for item in data:
        print("GROUP:", item.get("group"))
        print("TASK:", item.get("task"))
        print("STATUS:", item.get("status"))
        print("CONTENT:", item.get("content"))
        print("LATENCY:", item.get("latency"))
        print("MEMORY_BYTES:", item.get("memory_bytes"))
        print("CREATED_AT:", item.get("created_at"))
        print("UPDATE_AT:", item.get("update_at"))
        print("-" * 50)

    print("\n=== RESET TABLES ===")
    await watch_db.reset_tables()

    print("\n=== OBSERVABILITY AFTER RESET ===")
    print(await watch_db.observability.select())

    print("\n=== TESTE FINALIZADO ===")


if __name__ == "__main__":
    asyncio.run(test_watch_obs())
