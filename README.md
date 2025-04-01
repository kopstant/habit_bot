# Habit Bot

Бот для отслеживания привычек, построенный на Django.

## Описание

Habit Bot - это веб-приложение, которое помогает пользователям отслеживать и развивать полезные привычки. Приложение построено с использованием Django, PostgreSQL, Redis и Celery.

## Технологии

- Python 3.12
- Django 5.1.7
- PostgreSQL
- Redis
- Celery
- Docker

## Установка

1. Клонируйте репозиторий
2. Создайте файл .env на основе .env.sample
3. Запустите с помощью Docker Compose:
   ```bash
   docker compose up -d
   ```

## Разработка

Для запуска тестов:
```bash
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

## Требования

- Docker
- Docker Compose
- Python 3.12 (для локальной разработки)
- Poetry (для локальной разработки)

## Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/habit-bot.git
cd habit-bot
```

2. Создайте файл .env на основе .env.sample:
```bash
cp ..env.sample ..env
```

3. Запустите проект с помощью Docker Compose:
```bash
docker-compose up -d
```

4. Примените миграции:
```bash
docker-compose exec web poetry run python manage.py migrate
```

5. Создайте суперпользователя:
```bash
docker-compose exec web poetry run python manage.py createsuperuser
```

6. Соберите статические файлы:
```bash
docker-compose exec web poetry run python manage.py collectstatic --noinput
```

Проект будет доступен по адресу: http://localhost

## Разработка без Docker

1. Установите Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Установите зависимости:
```bash
poetry install
```

3. Активируйте виртуальное окружение:
```bash
poetry shell
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Запустите сервер разработки:
```bash
python manage.py runserver
```

## CI/CD

Проект настроен на автоматический деплой через GitHub Actions. При каждом пуше в ветку main:
1. Запускаются тесты и проверка кода
2. Собираются Docker-образы
3. Проект автоматически деплоится на сервер

### Настройка CI/CD

1. Добавьте следующие секреты в настройках GitHub репозитория:
   - `SERVER_HOST`: IP-адрес или домен сервера
   - `SERVER_USER`: имя пользователя на сервере
   - `SSH_PRIVATE_KEY`: приватный SSH-ключ для доступа к серверу

2. На сервере:
   - Установите Docker и Docker Compose
   - Создайте директорию для проекта
   - Настройте права доступа для пользователя деплоя

## Структура проекта

```
habit_bot/
├── config/             # Конфигурационные файлы
├── habit/             # Основное приложение
├── users/             # Приложение пользователей
├── manage.py          # Скрипт управления Django
├── pyproject.toml     # Зависимости проекта
├── poetry.lock        # Фиксация версий зависимостей
├── Dockerfile         # Конфигурация Docker
├── docker-compose.yml # Конфигурация Docker Compose
└── nginx.conf         # Конфигурация Nginx
```

## Лицензия

MIT 