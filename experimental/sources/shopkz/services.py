from typing import Type

from sqlalchemy.orm import Session

from experimental.sources import BaseServiceInterface
from experimental.sources.shopkz import ShopKZRepository
from experimental.sources.shopkz import models


class ShopKZService(BaseServiceInterface):
    name = 'shopkz'
    repo = ShopKZRepository()

    def create(self, session: Session, data: dict) -> models.Smartphone:
        return self.repo.create(session, data)

    def list(self, session: Session, **kwargs) -> list[Type[models.Smartphone]]:
        return self.repo.list(session, **kwargs)

    def get(self, session: Session, **kwargs) -> Type[models.Smartphone] | None:
        return self.repo.get(session, **kwargs)
