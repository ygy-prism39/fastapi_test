from sqlalchemy     import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .database  import Base

class Blog(Base):
    __tablename__ = 'blogs'

    id    = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    body  = Column(String(200))
    owner_id = Column(Integer, ForeignKey('persons.id'))

    creator = relationship("Person", back_populates="blogs")

class Person(Base):
    __tablename__ = 'persons'

    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String(200))
    email    = Column(String(1000))
    password = Column(String(2000))

    blogs = relationship("Blog", back_populates="creator")
