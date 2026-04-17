from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class UserData(BaseModel):
    age: int
    max_pulse: float

@app.get("/calculate")
def calculate(age: int):
    # Формула Хаскеля-Фокса
    max_p = 220 - age
    return {"max_pulse": max_p}

@app.post("/save")
def save(data: UserData):
    # Упрощенное сохранение в SQLite для примера
    return {"status": "saved", "data": data}
