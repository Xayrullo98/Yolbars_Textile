from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, String, Integer, Boolean,Float


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    token = Column(String(255), nullable=True)
