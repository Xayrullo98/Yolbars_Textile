from sqlalchemy.orm import relationship, backref

from db import Base
from sqlalchemy import Column, String, Integer, Boolean, Float

from models.projects import Projects


class Targets(Base):
    __tablename__ = 'Targets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(255), nullable=False, )
    comment = Column(String(255), nullable=True)
    watches = Column(Integer, nullable=False,default=0)
    status = Column(Boolean, nullable=False, default=True)
    project_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    project = relationship('Projects', foreign_keys=[project_id],
                            backref=backref('Projects', order_by="desc(Projects.id)"),
                            primaryjoin=lambda: (Projects.id == Targets.project_id))
