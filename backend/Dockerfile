# --- Этап 1: Сборка ---
FROM python:3.13-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
# Устанавливаем пакеты во временную папку
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- Этап 2: Финальный образ ---
FROM debian:bookworm-slim
WORKDIR /app
# Устанавливаем runtime-зависимости и curl
RUN apt-get update && apt-get install -y python3 python3-pip libpq5 curl && rm -rf /var/lib/apt/lists/*

# Копируем установленные пакеты из билдера
COPY --from=builder /install /usr/local
COPY . .

# Проверка работоспособности
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["/opt/venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]