"schema de observabilidade"

from pydantic import BaseModel
from typing import Literal


class CreateObs(BaseModel):

    task: str
    status: Literal["sucess", "pending", "failure"]
    content: str
    latency: int


class UpdateObs(BaseModel):

    task: str | None = None
    status: Literal["sucess", "pending", "failure"] | None = None
    content: str | None = None
    latency: int | None = None
