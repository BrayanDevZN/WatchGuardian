
"junta settings com token"

from src.core.module import Settings
from src.auth.token import JWT, logger
import uuid
class WatchAuth(JWT):

    def __init__(self, settings:Settings)-> None:

        secret = settings.required_secrets("secret")


        super().__init__(secret)

    #Gera uma secret se prescisar
    def secret(self) -> str:

        logger.info("Gerando uma secret...")

        secret = str(uuid.uuid8())

        logger.success("Secret gerada com sucesso!!")

        return secret




    