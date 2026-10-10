"rota de autenticacao"

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from jwt.exceptions import InvalidSignatureError

from src.service.module import WatchAuth, logger


auth_router = APIRouter(prefix="/auth", tags=["auth"])


# Gera um novo user token usando o refresh token e o user token antigo
@auth_router.post("/refresh")
async def refresh_user_token(request: Request) -> JSONResponse:

    logger.info("Gerando novo user token...")

    user_token = request.headers.get("X-user_token")
    refresh_token = request.headers.get("X-refresh_token")

    if user_token is None:
        raise HTTPException(
            status_code=401,
            detail="Expeted header 'X-user_token'"
        )

    if refresh_token is None:
        raise HTTPException(
            status_code=401,
            detail="Expeted header 'X-refresh_token'"
        )

    settings = request.app.state.settings
    auth = WatchAuth(settings=settings)

    try:
        user_payload = await auth.decode(user_token)
        refresh_payload = await auth.decode(refresh_token)

    except InvalidSignatureError:
        logger.error("Token invalido")

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    if user_payload.get("type") != "user_token":
        raise HTTPException(
            status_code=401,
            detail="Invalid X-user_token type"
        )

    if refresh_payload.get("type") != "refresh_token":
        raise HTTPException(
            status_code=401,
            detail="Invalid X-refresh_token type"
        )

    payload = dict(user_payload)
    payload.pop("exp", None)
    payload.pop("type", None)

    token = await auth.user_token(payload=payload)

    logger.success("Novo user token gerado com sucesso!!")

    return JSONResponse(
        status_code=201,
        content={
            "token": token
        }
    )
