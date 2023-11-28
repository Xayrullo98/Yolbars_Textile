from sqlalchemy.orm import relationship, backref

from db import Base
from sqlalchemy import Column, String, Integer, Boolean,Float

from models.categories import Categories


class Projects(Base):
    __tablename__ = 'Projects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False,)
    comment = Column(String(255), nullable=True)
    url = Column(String(255), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    source_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    source = relationship('Categories', foreign_keys=[source_id],
                            backref=backref('Categories', order_by="desc(Categories.id)"),
                            primaryjoin=lambda: (Categories.id == Projects.source_id))

