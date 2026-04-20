FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir \
    "pip>=25.0" \
    "wheel>=0.46.2" \
    "setuptools>=78.0" \
    "jaraco.context>=6.1.0" \
    "fastapi>=0.115.4" \
    "uvicorn[standard]>=0.30.0" \
    "psycopg2-binary>=2.9.9" \
    "prometheus-fastapi-instrumentator>=7.0.0"

# --- Финальный образ ---
FROM debian:bookworm-slim

WORKDIR /app

# Ставим Python из официального репо Debian — без лишних pip-пакетов в системе
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Берём только чистый venv — wheel и jaraco.context в системе вообще не существуют
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]