from operator import and_

from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import URLType

from db import Base
from sqlalchemy import Column, String, Integer, Boolean, Float, Text

from models.categories import Categories


class Category_items(Base):
    __tablename__ = 'Category_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=True, )
    status = Column(Boolean, nullable=False, default=True)
    category_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False,default=0)

    category = relationship('Categories', foreign_keys=[category_id],
                                  backref=backref('categories', order_by="desc(Categories.id)"),
                                  primaryjoin=lambda:(Categories.id == Category_items.category_id))

