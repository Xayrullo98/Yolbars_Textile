from typing import List, Optional
from pydantic import BaseModel


class CreateCategories(BaseModel):
    text: str
    category_id: int



class UpdateCategories(BaseModel):
    id: int
    category_id: int
    number: int
    status: bool