from typing import Type

from experimental.sources.BaseRepository import BaseRepositoryInterface
from experimental.sources.BaseSerivce import BaseServiceInterface
from experimental.sources.shopkz import ShopKZService
from experimental.exceptions import SourceNotFound


def get_source_service(name: str) -> Type[BaseServiceInterface]:
    source_service = (subclass for subclass in BaseServiceInterface.__subclasses__() if name == subclass.name)

    try:
        return next(source_service)
    except StopIteration:
        raise SourceNotFound(f'Source {name} not found.')
