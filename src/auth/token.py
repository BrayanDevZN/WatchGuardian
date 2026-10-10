"gera o token jwt"

from src.logs.module import Logs
logger = Logs(loglevel="SUCCESS")


import jwt
from jwt.exceptions import InvalidSignatureError

class JWT:

    def __init__(self, secret:str) -> None:

        self.secret = secret
        self.alg = "HS256"

    #Gera o token
    async def encode(self, payload:dict) -> str:

        try:

            logger.info("Criando token...")

            token=  jwt.encode(
                key=self.secret,
                algorithm=self.alg,
                payload=payload
            )

            logger.success("Token criado com sucesso!!")

            return token

        except Exception as error:

            logger.error(f"Erro ao gerar token: {error}")
            raise 

    async def decode(self, token:str) -> dict:

        try:

            logger.info("Decodificando token...")

            payload = jwt.decode(
                key=self.secret,
                algorithms=self.alg,
                jwt=token
            )

            logger.success("Toekn decodificado com sucesso!!")

            return payload

        except InvalidSignatureError as error:

            logger.error(f"Erro ao decodificar token: {error}")
            raise



        
