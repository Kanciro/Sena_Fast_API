from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mi Primera API")

class User(BaseModel):
    name: str
    age: int
    email: str

class Product(BaseModel):
    name: str
    id: int
    email: str
    price: float
    available: bool = True

@app.post("/users/")
def create_user(user: User):
    return {"name": user.name, "age": user.age, "email": user.email}

@app.get("/")
def hello_world() -> dict:
    return {"message": "¡Mi primera API FastAPI!"}


@app.get("/info")
def info() -> dict:
    return {"api": "FastAPI", "week": 1, "status": "running"}


@app.get("/greeting/{name}")
def greet_user(name: str) -> dict:
    return {"greeting": f"¡Hola {name}!"}

@app.get("/my-profile")
def my_profile(name:str, bootcamp:str, week: int, date:str, likes_fastapi:bool)-> dict:
    return {
        "name": name,
        "bootcamp": bootcamp,
        "week": week,
        "date": date,
        "likes_fastapi": likes_fastapi
    }

@app.get("/product/{product_id}")
def get_product(product_id: int) -> dict:
    return {"product_id": product_id, "message": "Product found!"}


