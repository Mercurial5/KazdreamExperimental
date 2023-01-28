from typing import Type

from sqlalchemy.orm import Session

from experimental.sources.shopkz import models
from experimental.sources.shopkz.models import Smartphone


class SmartphoneRepository:

    @staticmethod
    def create(session: Session, data: dict) -> models.Smartphone:
        smartphone = models.Smartphone(**data)
        session.add(smartphone)
        return smartphone

    @staticmethod
    def list(session: Session, **kwargs) -> list[Type[Smartphone]]:
        return session.query(models.Smartphone).filter_by(**kwargs).all()
