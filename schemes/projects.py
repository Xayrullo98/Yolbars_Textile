from typing import List
from pydantic import BaseModel


class CreateProject(BaseModel):
    name: str
    url: str
    source_id: int
    comment: str


class UpdateProject(BaseModel):
    id: int
    name: str
    url: str
    source_id: int
    comment: str
    status: bool