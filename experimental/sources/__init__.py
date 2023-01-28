from experimental.exceptions import SourceNotFound
from experimental.sources.BaseRepository import BaseRepositoryInterface
from experimental.sources.BaseSerivce import BaseServiceInterface
from experimental.utils import BaseParser

from experimental.sources import shopkz
from experimental.sources import technodom


def get_source_service(name: str) -> BaseServiceInterface:
    source_service = (subclass for subclass in BaseServiceInterface.__subclasses__() if name == subclass.name)

    try:
        return next(source_service)()
    except StopIteration:
        raise SourceNotFound(f'Source {name} not found.')


def get_source_parser(name: str) -> BaseParser:
    source_parser = (subclass for subclass in BaseParser.__subclasses__() if name == subclass.name)

    try:
        return next(source_parser)()
    except StopIteration:
        raise SourceNotFound(f'Source {name} not found.')
