"""Rotas do balanceador."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from src.logs.module import Logs


logger = Logs(loglevel="SUCCESS")
router = APIRouter(prefix="/balance", tags=["balance"])


async def _redirect(request: Request, path: str = "") -> RedirectResponse:
    try:
        url_server = request.state.url.rstrip("/")
        destination = f"{url_server}/{path.lstrip('/')}"
        if request.url.query:
            destination = f"{destination}?{request.url.query}"

        logger.info(f"Redirect to {destination}")
        return RedirectResponse(url=destination, status_code=307)
    except Exception as error:
        logger.error(f"Error: {error}")
        raise HTTPException(status_code=501, detail=str(error)) from error


@router.api_route("/", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def redirect_root(request: Request) -> RedirectResponse:
    return await _redirect(request)


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def redirect_path(request: Request, path: str) -> RedirectResponse:
    return await _redirect(request, path)
