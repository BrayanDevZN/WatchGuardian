"schema de observabilidade"

from pydantic import BaseModel
from typing import Literal


class CreateObs(BaseModel):

    task: str
    status: Literal["sucess", "pending", "failure"]
    content: str
    latency: int
    group: str
    memory_bytes: int = 0


class UpdateObs(BaseModel):

    task: str | None = None
    status: Literal["sucess", "pending", "failure"] | None = None
    content: str | None = None
    latency: int | None = None
    group: str | None = None
    memory_bytes: int | None = None
