![status](https://github.com/paveliglin89/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Проект «Foodgram» - продуктовый помощник

«Продуктовый помощник»: сайт, на котором пользователи могут публиковать 
рецепты, добавлять чужие рецепты в избранное и подписываться на публикации 
других авторов. Сервис «Список покупок» позволяет пользователям создавать 
список продуктов, которые нужно купить для приготовления выбранных блюд.

## Сслыка на проект и пользователи
* Ссылка на проект: (http://158.160.5.115/recipes)
 - Суперпользователь (логин/пароль): admin89 / admin89
 - Пользователь сайта 1 (e-mail/пароль): user1@user1.com / ryzenuser1
  - Пользователь сайта 2 (e-mail/пароль): user2@user2.com / ryzenuser2

## Технологии
* Python 3.8
* Django 4.0

## Ссылка на DockerHub

- firestar0502/foodgram

## Установка и запуск:

- Клонировать репозиторий и перейти в него в командной строке:

`git clone git@github.com:paveliglin89/foodgram-project-react.git
`
- Создать файл окружения .env с настройками БД:

Пример заполнения файла .env: 

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

- Сборка docker-compose:

`$ docker-compose up
` 

`$ docker-compose exec python manage.py makemigrations
`

`$ docker-compose exec python manage.py migrate
`

`$ docker-compose exec python manage.py createsuperuser
`

`$ docker-compose exec python manage.py collectstatic
`
- Заполнение базы ингредиентами:

```
$ python manage.py ingredients_manager
```

### Информация об авторе:
* [Pavel Iglin](https://github.com/paveliglin89)
