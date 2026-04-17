from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# РАЗРЕШАЕМ CORS (чтобы фронтенд мог достучаться до API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене тут должен быть конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserData(BaseModel):
    age: int
    max_pulse: float

@app.get("/calculate")
def calculate(age: int):
    max_p = 220 - age
    return {"max_pulse": max_p}

@app.post("/save")
def save(data: UserData):
    return {"status": "saved", "data": data}