# Базовый образ с Python 3.11
FROM python:3.11-slim

# Обновляем пакеты и ставим сборочные инструменты
RUN apt-get update && apt-get install -y build-essential python3-dev libffi-dev

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Запуск бота
CMD ["python", "bot.py"]
