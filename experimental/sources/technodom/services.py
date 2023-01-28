from typing import Type

from sqlalchemy.orm import Session

from experimental.sources import BaseServiceInterface
from experimental.sources.technodom import TechnodomRepository
from experimental.sources.technodom import models


class TechnodomService(BaseServiceInterface):
    name = 'technodom'
    repo = TechnodomRepository()

    def create(self, session: Session, data: dict) -> models.Smartphone:
        if self.repo.get(session, id=data['id']) is None:
            return self.repo.create(session, data)

    def list(self, session: Session, **kwargs) -> list[Type[models.Smartphone]]:
        return self.repo.list(session, **kwargs)

    def get(self, session: Session, **kwargs) -> Type[models.Smartphone] | None:
        return self.repo.get(session, **kwargs)
