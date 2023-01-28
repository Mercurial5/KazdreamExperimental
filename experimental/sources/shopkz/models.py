import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Smartphone(DeclarativeBase):
    id = sa.Column(sa.String(length=255), primary_key=True)
    name = sa.Column(sa.String())
    price = sa.Column(sa.Integer, index=True)
    memory = sa.Column(sa.String(length=20))
    created = sa.Column(sa.DateTime, server_default=func.now())
