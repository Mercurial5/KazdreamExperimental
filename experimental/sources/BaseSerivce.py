from __future__ import annotations

from typing import Protocol

from sqlalchemy.orm import Session

from experimental.sources.BaseRepository import BaseRepositoryInterface


class BaseServiceInterface(Protocol):
    repo: BaseRepositoryInterface

    def create(self, session: Session, data: dict):
        pass

    def list(self, session: Session, **kwargs):
        pass
