from typing import Protocol, Type

from sqlalchemy.orm import DeclarativeBase, Session


class BaseRepositoryInterface(Protocol):

    def create(self, session: Session, data: dict):
        pass

    def list(self, session: Session, **kwargs):
        pass
