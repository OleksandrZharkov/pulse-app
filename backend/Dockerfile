FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости и обновляем их до актуальных версий
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir \
    fastapi==0.110.0 \
    uvicorn[standard]==0.29.0 \
    psycopg2-binary==2.9.9 \
    prometheus-fastapi-instrumentator==7.0.0 \
    wheel==0.46.2 \
    jaraco.context==6.1.0

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]