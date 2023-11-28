from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import URLType

from db import Base
from sqlalchemy import Column, String, Integer, Boolean, Float, and_

from models.category_items import Category_items
from models.projects import Projects


class Uploaded_files(Base):
    __tablename__ = 'Uploaded_files'
    id = Column(Integer, primary_key=True, autoincrement=True)
    file = Column(URLType, nullable=False, )
    comment = Column(String(255), nullable=True)
    source = Column(String(255), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    source_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    category_source = relationship('Category_items', foreign_keys=[source_id],
                                   primaryjoin=lambda: and_(Category_items.id == Uploaded_files.source_id,
                                                            Uploaded_files.source == "category_item"),
                                   backref=backref("category_item_files"))

    project_source = relationship('Projects', foreign_keys=[source_id],
                                  primaryjoin=lambda: and_(Projects.id == Uploaded_files.source_id,
                                                           Uploaded_files.source == "project"),
                                  backref=backref("project_files"))
