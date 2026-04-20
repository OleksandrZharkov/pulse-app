FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Обновление pip и установка пакетов
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    "fastapi>=0.115.4" \
    "uvicorn[standard]>=0.30.0" \
    "psycopg2-binary>=2.9.9" \
    "prometheus-fastapi-instrumentator>=7.0.0" && \
    # Принудительное обновление уязвимых транзитивных зависимостей
    # CVE-2026-24049: wheel < 0.46.2
    # CVE-2026-23949: jaraco.context < 6.1.0
    pip install --no-cache-dir --upgrade \
    "wheel>=0.46.2" \
    "jaraco.context>=6.1.0"

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]