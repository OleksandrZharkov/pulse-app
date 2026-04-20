from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import os
import time
# Добавлен импорт для метрик
from prometheus_fastapi_instrumentator import Instrumentator 

app = FastAPI()

# Инициализация сбора метрик (должна быть до маршрутов)
Instrumentator().instrument(app).expose(app)

# Эндпоинт для проверки здоровья (Healthcheck)
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    attempts = 0
    while attempts < 10:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME", "postgres"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "password")
            )
            return conn
        except Exception as e:
            attempts += 1
            print(f"Попытка {attempts}: Ожидание БД... {e}")
            time.sleep(3)
    raise Exception("Не удалось подключиться к базе данных")

# Инициализация таблицы
conn = get_db_connection()
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS pulse_history (
        id SERIAL PRIMARY KEY, 
        age INT, 
        max_pulse FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.commit()
cur.close()
conn.close()

class UserData(BaseModel):
    age: int
    max_pulse: float

@app.get("/calculate")
def calculate(age: int):
    max_p = 220 - age
    return {"max_pulse": max_p}

@app.post("/save")
def save(data: UserData):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pulse_history (age, max_pulse) VALUES (%s, %s)", 
        (data.age, data.max_pulse)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "saved"}