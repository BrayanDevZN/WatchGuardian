"Le o token e valida ele"

from fastapi import HTTPException, Request
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from src.service.token import WatchAuth, logger


async def depends_user(request: Request):
    try:
        logger.info("Validating user...")

        settings = request.app.state.settings
        token = request.headers.get("X-user_token")

        if token is None:
            raise HTTPException(
                detail="Expeted header 'X-user_token'",
                status_code=401,
            )

        auth = WatchAuth(settings=settings)
        payload = await auth.decode(token)

        if payload.get("type") != "user_token":
            raise HTTPException(
                status_code=401,
                detail="Invalid X-user_token type",
            )

        return payload

    except ExpiredSignatureError:
        logger.error("Token expired.")
        raise HTTPException(
            status_code=401,
            detail="Expire X-user_token",
        )

    except InvalidSignatureError:
        logger.error("Invalid user.")
        raise HTTPException(
            status_code=401,
            detail="Invalid user",
        )

    except HTTPException:
        raise

    except Exception as error:
        logger.error(f"Failed to validate user: {error}")
        raise HTTPException(
            detail=str(error),
            status_code=401,
        )
