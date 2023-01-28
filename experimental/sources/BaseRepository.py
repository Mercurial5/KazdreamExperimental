from sqlalchemy.orm import Session


class BaseRepositoryInterface:

    @staticmethod
    def create(session: Session, data: dict):
        pass

    @staticmethod
    def list(session: Session, **kwargs):
        pass
