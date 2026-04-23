from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import os
import time
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator 

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Keep startup deterministic in CI by allowing tests to skip DB bootstrap.
    if not should_skip_db_init():
        init_db()
    yield

app = FastAPI(lifespan=lifespan)

Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def should_skip_db_init() -> bool:
    return os.getenv("SKIP_DB_INIT", "false").lower() == "true"

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
            # Retry helps when app starts before PostgreSQL is ready.
            print(f"Attempt {attempts}: waiting for database... {e}")
            time.sleep(3)
    raise Exception("Failed to connect to the database")

def init_db():
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