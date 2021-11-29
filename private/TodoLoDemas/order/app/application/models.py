from sqlalchemy import Column, DateTime, Integer, String, TEXT, ForeignKey, Float
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


class Order(BaseModel):
    STATUS_CREATED = "Created"
    STATUS_PENDING_ON_PAYMENT = "Pending on payment"
    STATUS_ACEPTED = "Acepted"
    STATUS_FINISHED = "Finished"
    STATUS_DECLINED = "Declined"
    ZIP_CODE_AR = 01
    ZIP_CODE_GI = 20
    ZIP_CODE_BI = 48

    __tablename__ = "manufacturing_order"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, nullable=False)
    number_of_pieces = Column(Integer, nullable=False)
    price_total = Column(Integer, nullable=False)
    description = Column(TEXT, nullable=False, default="No description")
    status = Column(String(256), nullable=False, default="Created")
    piezasConstruidas = Column(Integer, nullable=False, default=0)
    zip_code = Column(Integer, nullable=False)

    def as_dict(self):
        d = super().as_dict()
        return d
