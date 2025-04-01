from .settings import *

# Используем SQLite для тестов
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Отключаем Celery для тестов
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# Отключаем отправку уведомлений в тестах
TELEGRAM_BOT_TOKEN = "test_token"
