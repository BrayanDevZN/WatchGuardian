
"rota de logs"
from WatchGuardian._internal.auth.token import logger
from WatchGuardian._internal.service.db import WatchDb
from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder
from WatchGuardian._internal.server.depends import depends_user
from WatchGuardian._internal.server.schema.logs import CreateLog, UpdateLog
from fastapi.responses import JSONResponse
logs_router = APIRouter(prefix="/logs", tags=["logs"])


@logs_router.post("/")
async def create_log(log: CreateLog, request: Request, user: str | None = Depends(depends_user)) -> JSONResponse:
    logger.info("Registering log record...")

    settings = request.app.state.settings
    control_db = await WatchDb(settings=settings)

    log = await control_db.logs.create(log=log.log, status=log.status)
    await request.app.state.realtime_events.publish("logs.created", log)

    logger.success("Log record registered successfully.")
    return JSONResponse(status_code=201, content=jsonable_encoder(log))


@logs_router.get("/")
async def get_log(request: Request, id: int | None = None, public_id: str | None = None, user: str | None = Depends(depends_user)) -> JSONResponse:
    logger.info("Fetching log records...")

    settings = request.app.state.settings
    control_db = await WatchDb(settings=settings)

    result = await control_db.logs.select(public_id=public_id, id=id)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@logs_router.patch("/")
async def update_log(log: UpdateLog, request: Request, id: int | None = None, public_id: str | None = None, user: str | None = Depends(depends_user)) -> JSONResponse:
    logger.info("Updating log record...")

    settings = request.app.state.settings
    control_db = await WatchDb(settings=settings)

    result = await control_db.logs.update(public_id=public_id, id=id, log=log.log, status=log.status)
    if result is not None:
        await request.app.state.realtime_events.publish("logs.updated", result)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@logs_router.delete("/")
async def delete_log(request: Request, id: int | None = None, public_id: str | None = None, user: str | None = Depends(depends_user)) -> JSONResponse:
    logger.info("Deleting log record...")

    settings = request.app.state.settings
    control_db = await WatchDb(settings=settings)

    result = await control_db.logs.delete(public_id=public_id, id=id)
    if result is not None:
        await request.app.state.realtime_events.publish("logs.deleted", result)
    return JSONResponse(status_code=201, content="sucess")
