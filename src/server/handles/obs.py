"rota de observabilidade"
from src.auth.token import logger
from src.service.db import WatchDb
from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder
from src.server.depends import depends_user
from src.server.schema.obs import CreateObs, UpdateObs
from fastapi.responses import JSONResponse

obs_router = APIRouter(prefix="/obs", tags=["obs"])


# Rota pra criar observabilidade
@obs_router.post("/")
async def create_obs(obs: CreateObs, request: Request, user: str | None = Depends(depends_user)) -> JSONResponse:

    logger.info("Registrando observabilidade...")

    settings = request.app.state.settings

    control_db = await WatchDb(settings=settings)

    result = await control_db.observability.create(
        task=obs.task,
        status=obs.status,
        content=obs.content,
        latency=obs.latency
    )

    logger.success("Observabilidade registrada!!")

    return JSONResponse(status_code=201, content=jsonable_encoder(result))


# Rota pra ler observabilidade
@obs_router.get("/")
async def get_obs(
    request: Request,
    id: int | None = None,
    public_id: str | None = None,
    user: str | None = Depends(depends_user)
) -> JSONResponse:

    logger.info("Buscando observabilidade...")

    settings = request.app.state.settings

    control_db = await WatchDb(settings=settings)

    result = await control_db.observability.select(
        public_id=public_id,
        id=id
    )

    return JSONResponse(status_code=201, content=jsonable_encoder(result))


# Rota pra atualizar observabilidade
@obs_router.patch("/")
async def update_obs(
    obs: UpdateObs,
    request: Request,
    id: int | None = None,
    public_id: str | None = None,
    user: str | None = Depends(depends_user)
) -> JSONResponse:

    logger.info("Atualizando observabilidade...")

    settings = request.app.state.settings

    control_db = await WatchDb(settings=settings)

    result = await control_db.observability.update(
        public_id=public_id,
        id=id,
        task=obs.task,
        status=obs.status,
        content=obs.content,
        latency=obs.latency
    )

    return JSONResponse(status_code=201, content=jsonable_encoder(result))


# Rota pra deletar observabilidade
@obs_router.delete("/")
async def delete_obs(
    request: Request,
    id: int | None = None,
    public_id: str | None = None,
    user: str | None = Depends(depends_user)
) -> JSONResponse:

    logger.info("deletando observabilidade...")

    settings = request.app.state.settings

    control_db = await WatchDb(settings=settings)

    await control_db.observability.delete(
        public_id=public_id,
        id=id
    )

    return JSONResponse(status_code=201, content="sucess")
