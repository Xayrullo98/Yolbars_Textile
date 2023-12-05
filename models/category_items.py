from operator import and_

from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import URLType

from db import Base
from sqlalchemy import Column, String, Integer, Boolean, Float, Text

from models.projects import Projects


class Category_items(Base):
    __tablename__ = 'Category_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=True, )
    status = Column(Boolean, nullable=False, default=True)
    project_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False,default=0)

    project = relationship('Projects', foreign_keys=[project_id],
                                  backref=backref('projects', order_by="desc(Projects.id)"),
                                  primaryjoin=lambda:(Projects.id == Category_items.project_id))

