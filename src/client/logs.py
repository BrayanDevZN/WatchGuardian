"Cria a requisição para a url do servidor"

import requests
from src.logs.module import Logs 
logger = Logs(loglevel="SUCCESS")
from typing import Literal
class LogsClient:

    def __init__(self, url:str, token:str)-> None:

        self.url + "/logs"
        self.token = {"X-user_token": token}


    async def create_log(self, status:Literal["SUCCESS","INFO","WARNING","ERROR","DEBUG","CRITICAL"], log:str) -> dict:

        logger.info("Enviando requisição pro servidor para registrar log...")

        content = {
            "status":status,
            "log": log
        }

        response = requests.post(headers=self.token, json=content)

        if response.status_code > 400:

            logger.error(f"Houve um erro do status {response.status_code} ao registrar log: {response.text}")
            return

        data = response.json()

        return data

        