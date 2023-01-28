import sqlalchemy as sa
from sqlalchemy.sql import func

from config import Base


class Smartphone(Base):
    __tablename__ = 'shopkz_smartphone'

    id = sa.Column(sa.String(length=255), primary_key=True)
    name = sa.Column(sa.String())
    price = sa.Column(sa.Integer, index=True)
    memory = sa.Column(sa.String(length=20))
    created = sa.Column(sa.DateTime, server_default=func.now())
