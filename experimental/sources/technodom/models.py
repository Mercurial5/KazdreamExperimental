import sqlalchemy as sa
from sqlalchemy.sql import func

from config import Base


class Smartphone(Base):
    __tablename__ = 'technodom_smartphone'

    id = sa.Column(sa.String(length=255), primary_key=True)
    name = sa.Column(sa.String())
    price = sa.Column(sa.Integer, index=True)
    memory = sa.Column(sa.String(length=20))
    created = sa.Column(sa.DateTime(timezone=True), server_default=func.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
