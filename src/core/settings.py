"""
essa classe vai ler as variaveis de ambiente requeridas
"""


import os
from dotenv import load_dotenv
from typing import Any
class SettingsNotFoundEnv(Exception):
    pass

class SettingsNotFoundEnvironment(Exception):
    pass

class SettingsNotFoundConfig(Exception):
    pass

class Settings:

    def __init__(self, env_file:str|None=None)->None:

        self.secrets = {}
        self.configs = {}


        self.file = env_file
        self._get_env_file()

    #Le o env se for None
    def _get_env_file(self) -> None:

        if self.file is not None:

            if not os.path.exists(self.file):

                raise SettingsNotFoundEnvironment(f"Not found {self.file}")

            load_dotenv(self.file)

        else:

            load_dotenv()

    #Recebe uma lista de nome de variaveis de ambiente, e le, se for None, levanta erro, se não, adiciona em envs
    def required_secrets(self, envs:list[str]) -> None:

        for name in envs:

            env = os.getenv(name)

            if env is None or env == "":

                raise SettingsNotFoundEnv(f"Not found env {name}")

            self.secrets[name] = env 


    #Adiciona uma variavel de ambiente sem verificar se é none
    def add_secret(self, envs:str|list[str]) -> None:

        if isinstance(envs, str):

            self.secrets[envs] = os.getenv(envs)

        else:

            for name in envs:

                self.secrets[name] = os.getenv(name)


    #Pega uma secret
    def get_secret(self, secret_name:str) -> Any:

        if not secret_name in self.secrets.keys():

            raise SettingsNotFoundEnv(f"Not found {secret_name}")

        return self.secrets[secret_name]

    

    #Salva uma config por um dict
    def add_config(self, configs:dict|list[dict]) -> None:

        if isinstance(configs, dict):

            self.configs[configs["name"]] = configs["value"]

        else:

            for data in configs:

                self.configs[data["name"]] = data["value"]

    #Pega uma config opcional
    def get_config(self, name:str) -> Any:


        return self.configs[name] if name in self.configs.keys() else None 


    #pega uma config, e se for None, levanta erro
    def required_config(self, name:str) -> Any:

        if not name in self.configs.keys():

            raise SettingsNotFoundConfig(f"Not found config {name}")

        return self.configs[name]






            





    



    



    