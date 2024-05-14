# Используем базовый образ Python 3.10.12
FROM python:3.10.12-slim

# Устанавливаем зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем исходный код в контейнер
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Указываем порт, который будет использован
EXPOSE 5000

# Запускаем Flask приложение
CMD ["python", "app.py"]