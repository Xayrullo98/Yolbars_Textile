from typing import List
from pydantic import BaseModel


class CreateUser(BaseModel):
    name: str
    username: str
    password:str
    phone: str
    role: str


class UpdateUser(BaseModel):
    id: int
    name: str
    username: str
    phone: str
    role: str
    status: bool


class TokenUser(BaseModel):
    id: int
    username: str
    role: str
    token: str


class UserCurrent(BaseModel):
    id: int
    name: str
    username: str
    password: str
    role: str
    status: bool
