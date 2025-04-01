FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Установка рабочей директории
WORKDIR /lms

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock ./

# Установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копирование исходного кода
COPY . .

# Создание непривилегированного пользователя
RUN useradd -m appuser && chown -R appuser:appuser /lms
USER appuser

# Создание директорий для статических файлов и медиа
RUN mkdir -p /lms/staticfiles /lms/media

# Запуск приложения
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"] 
