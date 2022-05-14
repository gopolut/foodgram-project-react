![size](https://img.shields.io/github/languages/code-size/gopolut/foodgram-project-react)
![django version](https://img.shields.io/pypi/pyversions/Django)
![Django-app workflow](https://github.com/gopolut/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Документация к API дипломного проекта Foodgram (v1)

REST API для проекта **Foodgram**. Социальная сеть для любителей вкусно поесть и поделиться свими рецептами с миром.

> Для работы проекта необходим **Python 3.8**, **Django 2.2.27**, **Docker 4.6.1**, **Docker Compose v1.29.2**

> Полная документация: [51.250.29.69/redoc](http://51.250.29.69/redoc)

> Тестовые данные для проверки:

+ Администратор
```
username: root
password: **noclip2004**
```

+ Пользователь
```
username: semen
password: **qwerty34**
```

## Содержание
1. [Описание](#description)
2. [Запуск проекта](#launch)
3. [Примеры работы с API](#api_exaples)
4. [Об авторе](#about_author)

## <a name='description'>Описание</a>
Проект **Foodgram** - база данных рецептов, которые создают пользователи.

Позволяет создавать свои рецепты, делиться ими, добавлять в избранное рецепты других авторов, подписываться на авторов и следить за их обновлениями. Список ингредиентов, из рецептов добавленных в список покупок, можно скачать в формате .pdf.

API для сервиса **Foodgram** позволяет:

+ работать с пользователями:
  + регистрировать пользователей
  + получать и обновлять токены
  + удалять токены

+ создавать пользовательские роли:
  + Аноним
  + Аутентифицированный пользователь
  + Администратор

+ работать с рецептами:
  + получать список всех рецептов
  + получать конкретный рецепт по id
  + создавать рецепты
  + обновлять рецепты
  + удалять рецепты
  + Добавлять рецптам теги
  + Добавлять в рецпт ингредиенты

+ работать с избранным:
  + добавлять рецепты в избранное
  + удалять рецепты из избранного

+ работать со списками покупок:
  + добавлять рецепты в спискок покупок
  + удалять рецепты из списка покупок
  + скачивать список покупок в формате .pdf

+ работать с подписками на авторов:
  + подписываться на понравившихся авторов
  + отписываться от авторов


+ Получать список всех пользователей
+ Получать список всех тегов
+ Получать список всех ингредиентов


[Полная документация API (redoc.html)](https://github.com/gopolut/foodgram-project-react/blob/master/docs/redoc.html)

[⬆ Содержание](#Содержание)

## <a name='launch'>Запуск проекта</a>
Чтобы развернуть проект необходимо выполнить следующие действия (у Вас уже должен быть установлен Docker):

### Установка Docker и Docker Compose
Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Запуск проекта (на Linux)

- Склонируйте себе на компьютер проект `git clone git@github.com:gopolut/foodgram-project-react.git.`
- Создайте файл `.env` командой `touch .env` и добавьте в него переменные окружения для работы с базой данных:

```
  * echo DB_ENGINE=django.db.backends.postgresql
  * echo DB_NAME=postgres
  * echo POSTGRES_USER=postgres
  * echo POSTGRES_PASSWORD=postgres
  * echo DB_HOST=db
  * echo DB_PORT=5432
```

* Для запуска выполните команды:
  * `cd infra/`
  * `docker-compose up -d`
  * `docker-compose exec backend python manage.py migrate`
  * `docker-compose exec backend python manage.py createsuperuser`
  * `docker-compose exec backend python manage.py collectstatic --no-input`

* Загрузите тестовые данные:
  * `docker-compose exec backend python manage.py upload_data`

Проект будет доступен по адресу:
 * localhost/api/ - при локальной разработке
 * 51.250.99.212/ - рабочий проект

[⬆ Содержание](#Содержание)

## <a name='api_exaples'>Примеры работы с API</a>
**GET-запрос** на получение рецепта по id:

`/api/recipes/32`

```
{
    "id": 64,
    "tags": [
        {
            "id": 1,
            "name": "breakfast",
            "color": "#E26C2D",
            "slug": "breakfast"
        },
        {
            "id": 4,
            "name": "supper",
            "color": "#8100EA",
            "slug": "supper"
        }
    ],
    "ingredients": [
        {
            "id": 2376,
            "name": "вафли",
            "measurement_unit": "г",
            "amount": 500
        }
    ],
    "is_favorited": false,
    "is_in_shopping_cart": false,
    "author": {
        "email": "daddy@yandex.ru",
        "id": 35,
        "username": "dad",
        "first_name": "Иван",
        "last_name": "Иванов",
        "is_subscribed": true
    },
    "name": "Вафельное наслаждение",
    "image": "http://127.0.0.1:8000/media/recipes/%D0%B2%D0%B0%D1%84%D0%BB%D0%B8.jpeg",
    "text": "Процесс приготовления вафлей",
    "cooking_time": 3,
    "pub_date": "2022-05-12T21:39:58.899880Z"
}

```
**GET-запрос** на получение тегов:

`/api/tags/`

```
[
    {
        "id": 1,
        "name": "breakfast",
        "color": "#E26C2D",
        "slug": "breakfast"
    },
    {
        "id": 2,
        "name": "lunch",
        "color": "#00ff00",
        "slug": "lunch"
    },
    {
        "id": 3,
        "name": "dinner",
        "color": "#3b2fff",
        "slug": "dinner"
    }
]
```
**POST-запрос** на добавление произведения:

> Все поля являются обязательными

`/api/recipes/`

```
{
  "ingredients": [
    {
      "id": 130,
      "amount": 500
    },
    {
      "id": 737,
      "amount": 200
    }
  ],
  "tags": [
    4
  ],
 
  "name": "Торт шоколадный",
  "text": "Намазать бисквитные коржи кремом, подождать пока пропитаются",
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "cooking_time": 30
}

```

Выдача:

```
{
    "id": 69,
    "tags": [
        {
            "id": 1,
            "name": "breakfast",
            "color": "#E26C2D",
            "slug": "breakfast"
        }
    ],
    "ingredients": [
        {
            "id": 2319,
            "name": "бисквит шоколадный",
            "measurement_unit": "г",
            "amount": 500
        },
        {
            "id": 2926,
            "name": "крем заварной",
            "measurement_unit": "г",
            "amount": 200
        }
    ],
    "is_favorited": false,
    "is_in_shopping_cart": false,
    "author": {
        "email": "sem@yandex.ru",
        "id": 1,
        "username": "semen",
        "first_name": "Василий",
        "last_name": "Семенов",
        "is_subscribed": true
    },
    "name": "Торт шоколадный",
    "image": "http://127.0.0.1:8000/media/recipes/0208d61c-2b16-4a93-a08e-9439c1367320.png",
    "text": "Намазать бисквитные коржи кремом, подождать пока пропитаются",
    "cooking_time": 30,
    "pub_date": "2022-05-14T21:58:41.821304Z"
```

**Получение токена**

`/api/auth/token/login/`

```
{
  "password": "bopbop123",
  "email": "sem@yandex.ru"
}
```

Выдача:

```
{
    "auth_token": "123456789524e27df32aed868f000d11162d85d30"
}
```
-------------------------------------------------------
## <a name='about_author'>Об авторе</a>
Автор: [Лютиченко Павел](https://github.com/gopolut)
Контакты: motry@yandex.ru

[⬆ Содержание](#Содержание)

