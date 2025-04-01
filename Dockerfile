# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Создаем непривилегированного пользователя
RUN useradd -m appuser

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Настраиваем Poetry
RUN poetry config virtualenvs.create false

# Копируем файлы зависимостей
COPY --chown=appuser:appuser pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry install --no-interaction --no-ansi --no-root

# Копируем остальные файлы проекта
COPY --chown=appuser:appuser . .

# Переключаемся на непривилегированного пользователя
USER appuser

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"] 