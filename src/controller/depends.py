"Le o token e valida ele"

from fastapi import HTTPException, Depends, Request
from src.service.module import Settings, WatchAuth, logger
from jwt.exceptions import InvalidSignatureError
from datetime import datetime, timezone, timedelta
async def depends_user(request:Request):

    try:

        logger.info("Validando usuario...")

        settings = request.state.settings

        token = request.headers.get("Bearer X-user_token")

        if token is None:

            raise HTTPException(
                detail="Expeted header 'Bearer X-user_token'",
                status_code=401
            )

        auth = WatchAuth(settings=settings)


        token = await auth.decode(token)
        exp = datetime.strptime(token["exp"], "2026-10-10T18:30:00+00:00")
        now = datetime.now(timezone.utc)
        if now > exp:

            raise HTTPException(
                status_code=401,
                detail="Expire X-user_token"
            )

        



    except InvalidSignatureError:

        logger.error("Usuario invalido")

        raise HTTPException(
            status_code=401,
            detail="Invalid user"
        )

    except Exception as error:

        raise HTTPException(
            detail=error,
            status_code=501
        )



        

    