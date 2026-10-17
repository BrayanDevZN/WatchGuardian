"Cria a rota /balance"

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from src.logs.module import Logs 
logger = Logs(loglevel="SUCCESS")
router = APIRouter(prefix="/balance", tags=["balance"])

@router.api_route("/", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def redirect(request:Request) -> RedirectResponse:

    try:

        url = str(request.base_url).rstrip("/")
        url_server = request.state.url
      

        url = f"{url_server}{request.url.path}"

        logger.info(f"Redirect to {url}")

        return RedirectResponse(
            url=url,
            status_code=307
            
        )
    except Exception as error:

        logger.error(f"Error: {error}")
        raise HTTPException(error, status_code=501)



