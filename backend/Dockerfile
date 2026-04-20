FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создаём изолированный venv — полностью отдельный от системных пакетов
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Ставим свежий pip и wheel ПЕРВЫМИ, до любых других пакетов
RUN pip install --no-cache-dir \
    "pip>=25.0" \
    "wheel>=0.46.2" \
    "setuptools>=78.0" \
    "jaraco.context>=6.1.0"

# Теперь ставим основные зависимости — они уже не смогут понизить wheel/jaraco
RUN pip install --no-cache-dir \
    "fastapi>=0.115.4" \
    "uvicorn[standard]>=0.30.0" \
    "psycopg2-binary>=2.9.9" \
    "prometheus-fastapi-instrumentator>=7.0.0"

# --- Финальный образ ---
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем только чистый venv из builder-стадии, системные пакеты не едут
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]