
"rota de logs"
from src.service.module import logger, WatchDb
from fastapi import APIRouter, HTTPException, Request, Depends
from src.server.depends import depends_user
from src.server.schema.logs import CreateLog, UpdateLog
from fastapi.responses import JSONResponse
logs_router = APIRouter(prefix="/logs", tags=["logs"])


#Rota pra criar log
@logs_router.post("/")
async def create_log(log:CreateLog,request:Request,user:str|None=Depends(depends_user)) -> JSONResponse:

    logger.info("Registrando log...")

    settings = request.app.state.settings

    control_db = await WatchDb(settings=settings)

    log = await control_db.logs.create(log=log.log, status=log.status)

    logger.success("Log registrado!!")

    return JSONResponse(status_code=201, content=log)


#Rota pra ler os logs
@logs_router.get("/")
async def get_log(request:Request,id:int|None = None, public_id:str|None=None, user:str|None=Depends(depends_user)) -> JSONResponse:

    logger.info("Buscando log...")

    settings = request.app.state.settings

    control_db = await WatchDb(settings=settings)

    result = await control_db.logs.select(public_id=public_id, id=id)

    return JSONResponse(status_code=201, content=result)

#Rota pra atualizar os dados
@logs_router.patch("/")
async def update_log(log:UpdateLog,request:Request, id:int|None = None, public_id:str|None=None,  
                     user:str|None=Depends(depends_user)) -> JSONResponse:

    logger.info("Atualizando log...")


    settings = request.app.state.settings

    control_db = await WatchDb(settings=settings)

    result = await control_db.logs.update(public_id=public_id, id=id, log=log.log, status=log.status)

    return JSONResponse(status_code=201, content=result)


#Rota pra deletar 
@logs_router.delete("/")
async def delete_log(request:Request, id:int|None = None, public_id:str|None=None,  
                     user:str|None=Depends(depends_user)) -> JSONResponse:


    logger.info("deletando log...")


    settings = request.app.state.settings

    control_db = await WatchDb(settings=settings)

    await control_db.logs.delete(public_id=public_id, id=id)

    return JSONResponse(status_code=201, content="sucess")


    



    




    




    




