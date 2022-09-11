# Сервис Notifications - уведомления. Проектная работа 10 спринта.
[![Generic badge](https://img.shields.io/badge/Changelog-<COLOR>.svg)](./CHANGELOG.md)
[![Generic badge](https://img.shields.io/badge/Our-Team-<COLOR>.svg)](#команда)

Этот сервис будет слушать события от других компонентов системы и на их основе отправлять уведомления пользователям.
[Ссылка на приватный репозиторий с командной работой.](https://github.com/RuslanSibgatulin/notifications_sprint_1)


## Используемые технологии
- Код приложения на Python + fastapi.
- Транзакционное хранилище (OLTP) - Kafka.
- Брокер сообщений AMQP - RabbitMQ
- Сборщик логов - ELK.
- Все компоненты системы запускаются через Docker-compose.

# Запуск приложения
## Клонировать репозиторий
    git clone git@github.com:RuslanSibgatulin/notifications_sprint_1.git

## Подготовка окружения
### Подготовить файл с переменными окружения и сохранить под именем `docker/envs/prod`:

    KAFKA_HOST=broker
    KAFKA_PORT=29092

    LOGSTASH_HOST=logstash
    LOGSTASH_PORT=5044


## Запуск
Выполнить в терминале:

    make start

## Документация сервиса доступна по ссылке
- http://127.0.0.1:8000/api/openapi


# Команда
- [Ruslan Sibgatulin (lead)](https://github.com/RuslanSibgatulin)
- [Fedor Kuzminov](https://github.com/Riyce)