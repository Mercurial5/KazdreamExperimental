# KazdreamExperimental

Так как оригинальное задание показалось лёгким, решил сделать усложнённую версию, где я пытался применить как можно
больше своих знаний. В основном хотелось всё шаблонизировать, чтобы при добавлении новых ресурсов/источников не нужно
было писать новый код с нуля. Вместо сохранения в json файл применил SQLAlchemy (не flask_sqlalchemy) и Alembic.

# Installation

### Configure .env

Создайте файл `.env` и скопируйте туда значения из `.env.example`

### Build the image

```
docker compose build
```

### Run the container

```
docker compose up
```

## Usage

There are two endpoints, one for parsing and one for retrieving items:

* Parse items - `http://127.0.0.1:8000/sources/shopkz/parse`
* Retrieve items - `http://127.0.0.1:8000/sources/shopkz`

Note, that `/sources/shopkz/parse` may take some time.

## Explanation

При написании проекта старался придерживаться чистой архитектуры. Каждый
источник содержит в себе 4 модуля:

* models
* repositories
* services
* parser

### models

В этом модуле описана таблица содержащая все item-ы после парсинга

### repositories

Этот модуль работает с ORM и делает запросы

### services

В этом модуле можно описать проверку на дубликатов

### parser

Модуль, где описывается логика парсера

## Adding new source

Ниже приведён пример добавления нового источника https://www.technodom.kz/.

### Add Parser

Для начала нужно добавить новый package в `experimental/sources/` для нашего источника, назовём technodom.

Создадим модуль `TechnodomParser` и в нём класс с таким же именем который наследуется от BaseParser.

Теперь нужно переопределить абстрактные методы.

#### _get_base_link

По ссылке https://www.technodom.kz/catalog/smartfony-i-gadzhety/smartfony-i-telefony/smartfony видно, что сайт
использует пагинацию. Чтобы переходить по всем страницам, сохраним общую часть ссылки в переменную base_link, а
в методе _get_base_link будем возвращать эту ссылку со страницей:

```python
from typing import Any

from experimental.utils import BaseParser


class KaspiParser(BaseParser):

    def __init__(self):
        super().__init__()
        self.base_link = 'https://www.technodom.kz/catalog/smartfony-i-gadzhety/smartfony-i-telefony/smartfony?page='

    def _get_base_link(self, iteration: int) -> str:
        return self.base_link + str(iteration)

```

#### _fetch_raw_items

Теперь нужно написать инструкцию как забрать список `сырых` записей.

```python

from bs4 import BeautifulSoup

from experimental.utils import BaseParser


class KaspiParser(BaseParser):
    def __init__(self):
        super().__init__()
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
```

Один из способов понять, есть ли следующая страница, это посмотреть на количество найденных элементов.
Поэтому если элементов 0, значит этой страницы уже не существует.

#### _parse_raw_item

Теперь нужно описать как парсить один `сырой` элемент.

```python
import re

from bs4 import BeautifulSoup

from experimental.utils import BaseParser


class KaspiParser(BaseParser):
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
```

### Add model

Создаём модуль `models` и в нём описываем нашу модель:

```python
import sqlalchemy as sa
from sqlalchemy.sql import func

from config import Base


class Smartphone(Base):
    __tablename__ = 'technodom_smartphone'

    id = sa.Column(sa.String(length=255), primary_key=True)
    name = sa.Column(sa.String())
    price = sa.Column(sa.Integer, index=True)
    memory = sa.Column(sa.String(length=20))
    created = sa.Column(sa.DateTime(timezone=True), server_default=func.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
```

### Add layers

Теперь добавим слои репозитория и сервиса в модули `repositories` и `services`:

```python
from typing import Type

from sqlalchemy.orm import Session

from experimental.sources import BaseRepositoryInterface
from experimental.sources.technodom import models


class TechnodomRepository(BaseRepositoryInterface):

    @staticmethod
    def create(session: Session, data: dict) -> models.Smartphone:
        smartphone = models.Smartphone(**data)
        session.add(smartphone)
        return smartphone

    @staticmethod
    def list(session: Session, **kwargs) -> list[Type[models.Smartphone]]:
        return session.query(models.Smartphone).filter_by(**kwargs).all()

    @staticmethod
    def get(session: Session, **kwargs) -> models.Smartphone | None:
        return session.query(models.Smartphone).filter_by(**kwargs).first()
```

```python
from typing import Type

from sqlalchemy.orm import Session

from experimental.sources import BaseServiceInterface
from experimental.sources.technodom import TechnodomRepository
from experimental.sources.technodom import models


class TechnodomService(BaseServiceInterface):
    repo = TechnodomRepository()

    def create(self, session: Session, data: dict) -> models.Smartphone:
        if self.repo.get(session, id=data['id']) is None:
            return self.repo.create(session, data)

    def list(self, session: Session, **kwargs) -> list[Type[models.Smartphone]]:
        return self.repo.list(session, **kwargs)

    def get(self, session: Session, **kwargs) -> Type[models.Smartphone] | None:
        return self.repo.get(session, **kwargs)
```

### Alembic and migrations

Чтобы alembic увидел вашу модель и создал для неё миграцию, нужно в файле /alembic/env.py 
импортировать вашу модель:

```python
...

from experimental.sources.shopkz import models
from experimental.sources.technodom import models

...
```

И ввести команды:

> alembic revision --autogenerate -m "add technodom smartphone"

> alembic upgrade head

### Last step

Чтобы наш источник был виден для нашего скрипта (Для части api), нужно его импортировать в 
`/experimental/sources/__init__.py`:

```python
...

from experimental.sources import shopkz
from experimental.sources import technodom

...
```

Теперь `Сервисному слою` и нашему `парсеру` нужно дать одно имя, допустим `technodom`:

```python
...

class TechnodomParser(BaseParser):
    name = 'technodom'

...
```

```python
...

class TechnodomService(BaseServiceInterface):
    name = 'technodom'
    repo = TechnodomRepository()

...
```

### Testing

Перейдя по ссылке `http://127.0.0.1:8000/sources/technodom` мы увидим список смартфонов технодома.
Чтобы добавить туда смартфонов, нужно перейти по ссылке `http://127.0.0.1:8000/sources/technodom/parse`.


## About project

Этот проект вышел неудачным, так как код становится слишком тяжелым для такой простой задачи.
Главной причиной этому (по моему мнению) стала мало уделённого времени на продумывание структуры
проекта и его функционала.
