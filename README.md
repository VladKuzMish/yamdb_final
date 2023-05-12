# Проект YaMDB

### Описание
Проект YaMDB собирает отзывы пользователей на произведения (книги, фильмы, музыку). Сами произведения здесь не хранятся. Незарегистрированные пользователи могут просматривать информацию о произведениях, жанрах и категориях произведений, а также читать отзывы и комментарии.
Зарегистрированные пользователи могут оставлять отзывы и комментарии на произведения, а также выставлять оценку от 1 до 10. Право добавлять произведения, жанры и категории есть только у администраторов проекта. 

----

### Шаблон заполнения файла .env

В директорию infra необходимо добавить файл .env

----

### Как запустить проект локально:

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:VladKuzMish/yamdb_final.git
```

```
cd infra
```

Запустить docker-compose:

```
docker-compose up
```

После окончания сборки контейнеров выполнить миграции:
```
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Загрузить статику:

```
docker-compose exec web python manage.py collectstatic --no-input 
```

Заполнить базу данными:

```
docker-compose exec web python manage.py loaddata fixtures.json 
```

Проверить работу проекта по ссылке:

```
http://localhost/admin/ 
```
----

### Как запустить проект на боевом сервере:

Установить на сервере docker и docker-compose.
Скопировать на сервер файлы docker-compose.yaml и default.conf:
```
scp docker-compose.yaml <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/docker-compose.yaml
scp default.conf <логин_на_сервере>@<IP_сервера>:/home/<логин_на_сервере>/nginx/docker-compose.yaml
```

Добавить в Secrets на Github следующие данные:
```
DB_ENGINE=django.db.backends.postgresql # указать, что проект работает с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса БД (контейнера) 
DB_PORT=5432 # порт для подключения к БД
DOCKER_PASSWORD= # Пароль от аккаунта на DockerHub
DOCKER_USERNAME= # Username в аккаунте на DockerHub
HOST= # IP удалённого сервера
USER= # Логин на удалённом сервере
SSH_KEY= # SSH-key компьютера, с которого будет происходить подключение к удалённому серверу
PASSPHRASE= #Если для ssh используется фраза-пароль
TELEGRAM_TO= #ID пользователя в Telegram
TELEGRAM_TOKEN= #ID бота в Telegram
```

Выполнить команды:
* git add .
* git commit -m "<commit>"
* git push

После этого будут запущены процессы workflow:
* проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest
* сборка и доставка докер-образа для контейнера web на Docker Hub
* автоматический деплой проекта на боевой сервер
* отправка уведомления в Telegram о том, что процесс деплоя успешно завершился

После успешного завершения процессов workflow на боевом сервере необходимо выполнить следующие команды:
```
sudo docker-compose exec web python manage.py migrate
```
```
sudo docker-compose exec web python manage.py createsuperuser
```
```
sudo docker-compose exec web python manage.py collectstatic --no-input 
```

### В API доступны следующие эндпоинты:

* ```http://127.0.0.1:8000/api/v1/auth/signup/``` POST-запрос — получение кода подтверждения (confirmation_code) на указанный email.

* ```http://127.0.0.1:8000/api/v1/auth/token/``` POST-запрос — получение Access-токена в обмен на username и confirmation_code.

* ```http://127.0.0.1:8000/api/v1/users/``` Доступно для пользователей с ролью "администратор".
GET-запрос — получение списка всех пользователей, POST-запрос — добавление нового пользователя.

* ```http://127.0.0.1:8000/api/v1/users/{username}/``` Доступно для пользователей с ролью "администратор".
GET-запрос — получение пользователя по username.
PATCH-запрос — редактирование данных пользователя. DELETE-запрос — удаление пользователя.

* ```http://127.0.0.1:8000/api/v1/users/me/``` Права доступа — любой зарегистрированный пользователь.
GET-запрос — получение данных о своей учётной записи. PATCH-запрос — редактирование своей учётной записи.
Изменить роль пользователя нельзя.

* ```http://127.0.0.1:8000/api/v1/categories/``` GET-запрос — получение списка всех категорий (доступно без токена).
POST-запрос — создание новой категории (доступно для администратора).

* ```http://127.0.0.1:8000/api/v1/categories/{slug}/``` Доступно для пользователей с ролью "администратор".
DELETE-запрос — удаление категории по её slug.

* ```http://127.0.0.1:8000/api/v1/genres/``` GET-запрос — получение списка всех жанров (доступно без токена).
POST-запрос — добавление нового жанра (доступно для администратора).

* ```http://127.0.0.1:8000/api/v1/genres/{slug}/``` Доступно для пользователей с ролью "администратор".
DELETE-запрос — удаление жанра по его slug.

* ```http://127.0.0.1:8000/api/v1/titles/``` GET-запрос — получение списка всех произведений (доступно без токена).
POST-запрос — добавление нового произведения (доступно для администратора).

* ```http://127.0.0.1:8000/api/v1/titles/{titles_id}/``` GET-запрос — получение информации о произведении (доступно без токена).
PATCH-запрос — обновление информации о произведении (доступно для администратора).
DELETE-запрос — удаление произведения (доступно для администратора).

* ```http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/``` GET-запрос — получение списка всех отзывов (доступно без токена).
POST-запрос — добавление нового отзыва (доступно для аутентифицированных пользователей). Пользователь может оставить один отзыв на произведение.

* ```http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/``` GET-запрос — получение отзыва о произведении по его id (доступно без токена).
PATCH-запрос — изменение отзыва (доступно для администратора, модератора и автора отзыва).
DELETE-запрос — удаление отзыва по id (доступно для модератора, администратора и автора отзыва).

* ```http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/``` GET-запрос — получение списка комментариев к отзыву (доступно без токена).
POST-запрос — добавление комментария к отзыву (доступно для аутентифицированных пользователей). 

* ```http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/``` GET-запрос — получение информации о комментарии по id (доступно без токена).
PATCH-запрос — частичное обновление комментария (доступно для администратора, модератора и автора комментария).
DELETE-запрос — удаление комментария (доступно для администратора, модератора и автора комментария).

----


### Автор проекта

**Владислав Кузьмин.** 