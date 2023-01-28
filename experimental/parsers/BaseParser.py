from abc import ABC, abstractmethod
from typing import Any, Iterator

from experimental.parsers.utils import RequestWrapperInterface


class BaseParser(ABC):
    """
    Base class of all parsers.
    Implements the common parts of the code of every parser.
    """

    def __init__(self, request_wrapper: RequestWrapperInterface):
        self.request_wrapper = request_wrapper

    def parse_items(self) -> Iterator[Any]:
        iteration, has_next_iteration = 0, True

        while has_next_iteration:
            link = self._get_base_link(iteration)

            has_next_iteration, raw_items = self._fetch_raw_items(link)
            raw_items = self._filter_raw_items(raw_items)

            items = [self._parse_raw_item(raw_item) for raw_item in raw_items]
            items = self._filter_items(items)

            iteration += 1

            yield from items

    @abstractmethod
    def _get_base_link(self, iteration: int) -> str:
        """
        Returns the link where list of items is stored.

        With the help of parameter `iteration` we can iterate through pages or categories. Examples:

        1)
        self.base_link = 'https://some-site.com/items?page=
        return self.base_link + str(iteration)

        2)
        self.base_links = ['link-to-category-1', 'link-to-category-2', ...]
        return self.base_links[iteration]

        :param iteration: int
        :return: str
        """

    @abstractmethod
    def _fetch_raw_items(self, link: str) -> tuple[bool, list[Any]]:
        """
        Sends request to link where list of items is stored and returns them as list.
        Items in the list are considered `raw`. `raw` items needs to be parsed to use them.

        If there is another iteration, returns True as a first parameter of tuple. Otherwise, False.

        :param link: str
        :return: tuple[bool, list[Any]]
        """

    @abstractmethod
    def _parse_raw_item(self, raw_item: Any) -> Any:
        """
        Takes raw_item and parses it to return `cleaned` item, which can be used to store in DB, for example.

        :param raw_item: Any
        :return: Any
        """

    @staticmethod
    def _filter_raw_items(raw_items: list[Any]) -> list[Any]:
        return raw_items

    @staticmethod
    def _filter_items(items: list[Any]) -> list[Any]:
        return items
