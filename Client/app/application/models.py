from sqlalchemy import Column, DateTime, Integer, String, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        fields = ""
        for c in self.__table__.columns:
            if fields == "":
                fields = "{}='{}'".format(c.name, getattr(self, c.name))
            else:
                fields = "{}, {}='{}'".format(fields, c.name, getattr(self, c.name))
        return "<{}({})>".format(self.__class__.__name__, fields)

    @staticmethod
    def list_as_dict(items):
        return [i.as_dict() for i in items]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Client(BaseModel):

    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(TEXT, nullable=False, default="No name")
    surname = Column(TEXT, nullable=False, default="No surname")
    password = Column(TEXT, nullable=False, default="No password")
    nickname = Column(TEXT, nullable=False, default="No nickname", unique=True)
    role_id = Column(Integer, ForeignKey('roles.id'))

class Role(BaseModel):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(TEXT, nullable=False, default="No name")
    permisions = Column(TEXT, nullable=False, default="No permisions")
    client = relationship("Client")

