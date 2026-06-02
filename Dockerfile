# Базовый образ Python
FROM python:3.11-slim

# Рабочая директория (используем имя, отличное от пакета app, чтобы избежать конфликтов импорта)
WORKDIR /app_project

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=1000 --retries 10 -r requirements.txt



COPY . .

# Устанавливаем PYTHONPATH в текущую рабочую директорию
ENV PYTHONPATH=/app_project

# Запуск через gunicorn для продакшена
# Gunicorn будет искать модуль 'app' внутри /app_project
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.main:app"]
