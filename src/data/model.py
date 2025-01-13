from data.init import Base, engine
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func


class Creature(Base):
    __tablename__ = "creature"

    name = Column(String, primary_key=True)
    description = Column(String)
    country = Column(String)
    area = Column(String)
    aka = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class Explorer(Base):
    __tablename__ = "explorer"

    name = Column(String, primary_key=True)
    country = Column(String)
    description = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class User(Base):
    __tablename__ = "user"

    name = Column(String, primary_key=True)
    hash_ = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class XUser(Base):
    __tablename__ = "xuser"

    name = Column(String, primary_key=True)
    hash_ = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


Base.metadata.create_all(bind=engine)
