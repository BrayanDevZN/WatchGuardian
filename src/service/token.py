
"junta settings com token"

from src.core.module import Settings
from src.auth.token import JWT, logger
import uuid
class WatchAuth(JWT):

    def __init__(self, settings:Settings|None=None)-> None:

        secret = settings.get_secret("secret") if settings is not None else None

        if secret is not None:
            super().__init__(secret)

    #Gera uma secret se prescisar
    def secret(self) -> str:

        logger.info("Gerando uma secret...")

        secret = str(uuid.uuid8())

        logger.success("Secret gerada com sucesso!!")

        return secret




    