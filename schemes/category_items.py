from typing import List, Optional
from pydantic import BaseModel


class CreateCategories(BaseModel):
    text: str
    project_id: int



class UpdateCategories(BaseModel):
    id: int
    project_id: int
    number: int
    status: bool