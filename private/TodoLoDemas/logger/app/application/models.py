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


class Log(BaseModel):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    __tablename__ = "log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(TEXT, nullable=False)
    url = Column(TEXT, nullable=False)
    request_body = Column(TEXT, nullable=False)
    service = Column(TEXT, nullable=False)
    service_id = Column(Integer, nullable=False)
    severity = Column(TEXT, nullable=False)
    filename = Column(TEXT, nullable=True)
    function = Column(TEXT, nullable=True)
    message = Column(TEXT, nullable=False)
