from sqlalchemy.orm import Session

from experimental.sources import BaseRepositoryInterface
from experimental.sources.shopkz import ShopKZRepository
from experimental.sources.shopkz import models


class ShopKZService:
    repo: BaseRepositoryInterface = ShopKZRepository()

    def create(self, session: Session, data: dict) -> models.Smartphone:
        return self.repo.create(session, data)

    def list(self, session: Session, **kwargs) -> list[models.Smartphone]:
        return self.repo.list(session, **kwargs)
