# --- Этап сборки (Builder) ---
FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем только файл зависимостей сначала — это ускорит сборку (кеширование)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Финальный образ (Final) ---
FROM debian:bookworm-slim

WORKDIR /app

# Ставим только runtime-зависимости (никаких компиляторов)
RUN apt-get update && apt-get install -y \
    python3 \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Копируем чистый venv из билдера
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]