from typing import List, Optional
from pydantic import BaseModel


class CreateTarget(BaseModel):
    link: str
    comment: Optional[str]=''
    project_id: int


class UpdateTarget(BaseModel):
    id: int
    link: str
    comment: Optional[str] = ''
    project_id: int
    status: bool