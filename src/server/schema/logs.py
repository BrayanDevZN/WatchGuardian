"schema de logs"

from pydantic import BaseModel
from typing import Literal

class CreateLog(BaseModel):

    status: Literal["SUCCESS","INFO","WARNING","ERROR","DEBUG","CRITICAL"]
    log: str


class UpdateLog(BaseModel):


    log: str | None = None
    status: Literal["SUCCESS","INFO","WARNING","ERROR","DEBUG","CRITICAL"] | None = None