FROM python:3.11-slim
WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Добавлена библиотека prometheus-fastapi-instrumentator
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    psycopg2-binary \
    prometheus-fastapi-instrumentator

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]