from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from db import Base
from sqlalchemy import Column, String, Integer, Boolean, Float, Text


class Categories(Base):
    __tablename__ = 'Categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, )
    status = Column(Boolean, nullable=False, default=True)
    comment = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=False)
