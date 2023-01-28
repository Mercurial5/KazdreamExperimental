from typing import Protocol

from sqlalchemy.orm import Session


class BaseRepositoryInterface(Protocol):

    def create(self, session: Session, data: dict):
        pass

    def list(self, session: Session, **kwargs):
        pass
