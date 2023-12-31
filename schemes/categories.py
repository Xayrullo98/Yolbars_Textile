from typing import List, Optional
from pydantic import BaseModel


class CreateCategories(BaseModel):
    name: str
    comment: Optional[str]=''
    


class UpdateCategories(BaseModel):
    id: int
    name: str
    comment: Optional[str] = ''
    status: bool