
from unicodedata import name
from .. import db, flask_bcrypt
import datetime
from sqlalchemy.sql import func, delete
from app.main.model.blacklist import BlacklistToken
from ..config import key
import jwt
from typing import Union
from .base import Base, TimestampMixin

class Category(db.Model, Base, TimestampMixin):
    """ Category Model for storing product category """
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<id: category: {}'.format(self.name)

    @staticmethod
    def check_category(name: str) -> bool:
        res = Category.query.filter_by(name=str(name)).first()
        if res:
            return True
        else:
            return False

    