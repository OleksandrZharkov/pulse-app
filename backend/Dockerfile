# --- Этап 1: Сборка ---
FROM python:3.13-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Создаем venv
RUN python -m venv /opt/venv
# Устанавливаем переменные окружения для этапа сборки
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Этап 2: Финальный образ ---
FROM debian:bookworm-slim

WORKDIR /app

# Устанавливаем runtime-зависимости + curl
RUN apt-get update && apt-get install -y python3 libpq5 curl && rm -rf /var/lib/apt/lists/*

# Копируем venv из билдера
COPY --from=builder /opt/venv /opt/venv

# !!! САМОЕ ВАЖНОЕ: Указываем PATH для финального образа !!!
# Теперь система будет искать бинарники в /opt/venv/bin автоматически
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

# Теперь uvicorn будет найден автоматически благодаря ENV PATH
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]