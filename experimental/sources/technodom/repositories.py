from typing import Type

from sqlalchemy.orm import Session

from experimental.sources import BaseRepositoryInterface
from experimental.sources.technodom import models


class TechnodomRepository(BaseRepositoryInterface):

    @staticmethod
    def create(session: Session, data: dict) -> models.Smartphone:
        smartphone = models.Smartphone(**data)
        session.add(smartphone)
        return smartphone

    @staticmethod
    def list(session: Session, **kwargs) -> list[Type[models.Smartphone]]:
        return session.query(models.Smartphone).filter_by(**kwargs).all()

    @staticmethod
    def get(session: Session, **kwargs) -> models.Smartphone | None:
        return session.query(models.Smartphone).filter_by(**kwargs).first()
