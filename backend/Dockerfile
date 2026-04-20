# --- Этап 1: Сборка (Builder) ---
FROM python:3.13-slim AS builder

WORKDIR /app

# Устанавливаем системные зависимости для компиляции
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создаем venv с флагом --copies, чтобы файлы были доступны после копирования между этапами
RUN python -m venv --copies /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Этап 2: Финальный образ (Final) ---
FROM debian:bookworm-slim

WORKDIR /app

# Устанавливаем только runtime-зависимости + curl для healthcheck
RUN apt-get update && apt-get install -y \
    python3 \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем venv из этапа сборки
COPY --from=builder /opt/venv /opt/venv

# Прописываем путь к venv в переменные окружения
ENV PATH="/opt/venv/bin:$PATH"

# Копируем код приложения
COPY . .

# Проверка работоспособности
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

# Запуск через полный путь для надежности
CMD ["/opt/venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]