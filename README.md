# KazdreamExperimental

Так как оригинальное задание показалось лёгким, решил сделать усложнённую версию, где я пытался применить как можно
больше своих знаний. В основном хотелось всё шаблонизировать, чтобы при добавлении новых ресурсов/источников не нужно
было писать новый код с нуля. Вместо сохранения в json файл применил SQLAlchemy (не flask_sqlalchemy) и Alembic.

# Installation

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

* Parse items - http://127.0.0.1:8000/sources/shopkz/parse
* Retrieve items - http://127.0.0.1:8000/sources/shopkz

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

