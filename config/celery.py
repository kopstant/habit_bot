from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from dotenv.main import load_dotenv

# Установка переменной окружения для настроек проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Создание экземпляра объекта Celery
app = Celery("config")

# Явные настройки Redis
app.conf.broker_url = "redis://redis:6379/0"
app.conf.result_backend = "redis://redis:6379/0"
app.conf.broker_connection_retry_on_startup = True

# Загрузка настроек из файла Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Загружаем переменные из .env после всех настроек
load_dotenv()

# Настройка часового пояса
app.conf.timezone = settings.TIME_ZONE

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks(["habit", "users"])


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
