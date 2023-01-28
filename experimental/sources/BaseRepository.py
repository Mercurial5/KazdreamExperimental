from sqlalchemy.orm import Session


class BaseRepositoryInterface:
    """
    Clean architecture - repository layer
    """

    @staticmethod
    def create(session: Session, data: dict):
        pass

    @staticmethod
    def list(session: Session, **kwargs):
        pass

    @staticmethod
    def get(session: Session, **kwargs):
        pass
