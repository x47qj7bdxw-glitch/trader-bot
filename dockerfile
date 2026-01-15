# Используем стабильный Python 3.10
FROM python:3.10-slim

# Устанавливаем зависимости для Pyrogram
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую папку
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем pip-зависимости
RUN pip install --no-cache-dir tgcrypto python-dotenv
RUN pip install --no-cache-dir git+https://github.com/pyrogram/pyrogram.git@master

# Команда запуска
CMD ["python", "userbot.py"]
