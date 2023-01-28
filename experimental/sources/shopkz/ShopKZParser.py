import json
import re

from bs4 import BeautifulSoup

from experimental.utils import BaseParser


class ShopKZParser(BaseParser):
    name = 'shopkz'

    def __init__(self):
        super().__init__()
        self.base_link = 'https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'

        self.headers = {
            'User-Agent': 'let me in'
        }

    def _get_base_link(self, iteration: int) -> str:
        return self.base_link + f'?PAGEN_1={iteration + 1}'

    def _fetch_raw_items(self, link: str) -> tuple[bool, list[str]]:
        response = self.request_wrapper.send('GET', link, headers=self.headers)
        if response['status'] is False:
            # Instead of printing it, we could log this or send notification
            print(response['error'])
            return False, []

        soup = BeautifulSoup(response['content'], 'html.parser')

        next_link = soup.find('link', attrs={'rel': 'next'})
        has_next_page = next_link is not None

        items = soup.find_all('div', attrs={'class': 'bx_catalog_item_container gtm-impression-product'})
        items = [item['data-product'] for item in items]

        return has_next_page, items

    def _parse_raw_item(self, raw_item: str) -> dict:
        data = json.loads(raw_item)
        return {
            'id': data['item_id'],
            'name': data['item_name'],
            'price': int(data['price']),
            'memory': self._parse_memory(data['item_name'])
        }

    @staticmethod
    def _parse_memory(name: str) -> str:
        """
        The safest method to parse memory would be this one:

        Go to the smartphone page* and find key `a_OPERATIVE_MEMORRY`, which has correct memory size.
        But this method requires us to make a request (1) and parse html tree (2).
        And considering amount of phones the time to parse each phone will sum-up and will slow the parsing overall.

        This is why I decided to use regular expressions, because every phone has memory-size in their names.

        * view-source:https://shop.kz/offer/smartfon-vivo-v21-128gb-sunset-dazzle-v2066-sn-869963059110154/

        Note:
        To make this method perfect, we could add one condition. If regular expression found memory size and
        didn't raise any errors, it will just return the memory size. Otherwise, it would make a request and
        took memory size from the `a_OPERATIVE_MEMORRY` key.

        P.S. I didn't make this method `perfect` because it worked this way anyway.
        P.S.S. And it also would make my code `dirtier`. (Too long to explain...)

        :param name: str
        :return: str
        """
        return re.search(r'(\d+)\s*[TG][Bb]', name).group()
