from sqlalchemy import BigInteger, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func
from .. import db

class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(cls=Base)

class TimestampMixin(object):
    created_at = db.Column(DateTime, default=func.now())
    updated_at = db.Column(DateTime, default=func.now())