from __future__ import annotations

from sqlalchemy.orm import Session

from experimental.sources.BaseRepository import BaseRepositoryInterface


class BaseServiceInterface:
    repo: BaseRepositoryInterface
    name = None

    def create(self, session: Session, data: dict):
        pass

    def list(self, session: Session, **kwargs):
        pass

    def get(self, session: Session, **kwargs):
        pass
