import re

from bs4 import BeautifulSoup

from experimental.utils import BaseParser


class TechnodomParser(BaseParser):
    name = 'technodom'

    def __init__(self):
        super().__init__()
        self.domain = 'https://www.technodom.kz'
        self.base_link = 'https://www.technodom.kz/catalog/smartfony-i-gadzhety/smartfony-i-telefony/smartfony?page='

    def _get_base_link(self, iteration: int) -> str:
        return self.base_link + str(iteration)

    def _fetch_raw_items(self, link: str) -> tuple[bool, list[str]]:
        response = self.request_wrapper.send('GET', link)
        if not response['status']:
            # Instead of printing we could log it or send notification
            print(response['error'])
            return False, []

        soup = BeautifulSoup(response['content'], 'html.parser')
        items = soup.find_all('a', attrs={'class': 'category-page-list__item-link'})

        if len(items) == 0:
            return False, []

        return True, [item['href'] for item in items]

    def _parse_raw_item(self, raw_item: str) -> dict:
        response = self.request_wrapper.send('GET', f'{self.domain}{raw_item}')
        if not response['status']:
            # Instead of printing we could log it or send notification
            print(response['error'])
            return {}

        soup = BeautifulSoup(response['content'], 'html.parser')

        item_id = soup.find('p', attrs={'class': 'Typography product-info__sku Typography__Caption'}).text
        item_id = int(item_id.replace('Артикул: ', ''))

        name = soup.find('h1', attrs={'class': 'Typography Typography__Title Typography__Title_Small'}).text
        price = soup.find('div', attrs={'class': 'product-actions__price product-prices'}).p.text
        memory = re.search(r'(\d+)\s*[TG][Bb]', name).group()

        return {
            'id': item_id,
            'name': name,
            'price': price,
            'memory': memory
        }
