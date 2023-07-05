# electronics_django

Web application of the network for the sale of electronics

## Установка

0. Склиноровать проект
1. `pipenv install`
2. Заполнить .env файл по шаблону .env_example

## Подключение к PostgreSQL БД

1. Создать pg_service.conf файл. Узнать папку, куда нужно поместить данный файл можно с помощью команды
   pg_config --sysconfdir (по умолчанию /etc/postgresql-common)
2. Создать .pgpass файл и поместить в корень папки проекта.
   Шаблоны для создания файлов - https://docs.djangoproject.com/en/4.1/ref/databases/#postgresql-connection-settings
3. После подключения к БД выполнить команду `python manage.py migrate`

## Celery and RabbitMQ

1. В качестве брокера используется RabbitMQ, url к нему нужно указать в .env файле.
2. Установка актуальной версии RabbitMQ на ubuntu Linux - https://www.rabbitmq.com/install-debian.html#apt-cloudsmith
3. Запуск rabbitmq сервера - `sudo rabbitmq-server`, остановка - `sudo rabbitmqctl stop`
4. После запуска необходимо выполнить настройку сервера для подключения к
   celery - https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/rabbitmq.html#setting-up-rabbitmq
5. Запустить celery - `celery -A electronics_sales worker`
6. Запустить celery beat - `celery -A electronics_sales beat`

## Отправка email

1. Для отправки писем используется SMPT сервер mail.ru
2. В `EMAIL_HOST_PASSWORD` из .env файла необходимо указать пароль для внешних приложений, как
   сгенерировать - https://help.mail.ru/mail/security/protection/external

## Endpoints

Ссылка на endpoints http://127.0.0.1:8000/api/docs/