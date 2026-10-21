"rota de observabilidade"
from WatchGuardian._internal.auth.token import logger
from WatchGuardian._internal.service.db import WatchDb
from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder
from WatchGuardian._internal.server.depends import depends_user
from WatchGuardian._internal.server.schema.obs import CreateObs, UpdateObs
from fastapi.responses import JSONResponse

obs_router = APIRouter(prefix="/obs", tags=["obs"])


@obs_router.post("/")
async def create_obs(obs: CreateObs, request: Request, user: str | None = Depends(depends_user)) -> JSONResponse:
    logger.info("Registering observability record...")

    settings = request.app.state.settings
    control_db = await WatchDb(settings=settings)

    result = await control_db.observability.create(
        group=obs.group,
        task=obs.task,
        status=obs.status,
        content=obs.content,
        latency=obs.latency,
        memory_bytes=obs.memory_bytes,
    )
    await request.app.state.realtime_events.publish("observability.created", result)

    logger.success("Observability record registered successfully.")
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@obs_router.get("/")
async def get_obs(
    request: Request,
    id: int | None = None,
    public_id: str | None = None,
    group: str | None = None,
    user: str | None = Depends(depends_user),
) -> JSONResponse:
    logger.info("Fetching observability records...")

    settings = request.app.state.settings
    control_db = await WatchDb(settings=settings)

    result = await control_db.observability.select(
        public_id=public_id,
        id=id,
        group=group,
    )
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@obs_router.patch("/")
async def update_obs(obs: UpdateObs, request: Request, id: int | None = None, public_id: str | None = None, user: str | None = Depends(depends_user)) -> JSONResponse:
    logger.info("Updating observability record...")

    settings = request.app.state.settings
    control_db = await WatchDb(settings=settings)

    result = await control_db.observability.update(
        public_id=public_id,
        group=obs.group,
        id=id,
        task=obs.task,
        status=obs.status,
        content=obs.content,
        latency=obs.latency,
        memory_bytes=obs.memory_bytes,
    )
    if result is not None:
        await request.app.state.realtime_events.publish("observability.updated", result)

    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@obs_router.delete("/")
async def delete_obs(request: Request, id: int | None = None, public_id: str | None = None, user: str | None = Depends(depends_user)) -> JSONResponse:
    logger.info("Deleting observability record...")

    settings = request.app.state.settings
    control_db = await WatchDb(settings=settings)

    result = await control_db.observability.delete(public_id=public_id, id=id)
    if result is not None:
        await request.app.state.realtime_events.publish("observability.deleted", result)
    return JSONResponse(status_code=201, content="sucess")
