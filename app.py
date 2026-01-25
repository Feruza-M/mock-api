from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import random
from typing import List, Dict, Any
from datetime import datetime

app = FastAPI(title="Mock API for Orders, Users, Catalog")

class Order(BaseModel):
    id: str
    status: str
    name: str

class User(BaseModel):
    id: str
    username: str

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

# Список товаров для детейлинга авто (на основе популярных продуктов)
CATALOG: List[Dict[str, Any]] = [
    {"id": 1, "name": "Низкопенный шампунь Rapid", "description": "Шампунь для ручной мойки без смывания", "price": 1500.0},
    {"id": 2, "name": "Очиститель Auto Finesse Dynamite", "description": "Концентрированный очиститель для экстерьера", "price": 2200.0},
    {"id": 3, "name": "Микрофибра короткий ворс", "description": "Зеленая микрофибра 40x40 см для сушки", "price": 500.0},
    {"id": 4, "name": "MotorCleaner гель", "description": "Очиститель двигателя 750 мл", "price": 1200.0},
    {"id": 5, "name": "Pure Wheels+ концентрат", "description": "Очиститель шин и дисков 500 мл", "price": 1800.0},
    {"id": 6, "name": "Ultra Safe бесконтактный шампунь", "description": "Шампунь 1 л для экстерьера", "price": 900.0},
    {"id": 7, "name": "GYEON Q² Mohs EVO", "description": "Керамическое покрытие до 3 лет", "price": 5000.0},
    {"id": 8, "name": "DETAIL Quick Detailer", "description": "Универсальный быстрый очиститель", "price": 1100.0},
    {"id": 9, "name": "Shine Systems GlassCleaner", "description": "Стеклоочиститель без разводов", "price": 700.0},
    {"id": 10, "name": "CarPro Perl", "description": "Защита пластика и резины с УФ-фильтром", "price": 1400.0},
]

statuses = ["new", "processing", "shipped", "delivered", "cancelled"]
order_names = ["iPhone 15", "Samsung TV", "Nike Shoes", "Laptop Dell", "Headphones Sony"]
usernames = ["user123", "admin456", "guest789", "john_doe", "jane_smith", "devops_guru"]

@app.get("/order", response_model=Order)
def get_order() -> Order:
    return Order(
        id=str(uuid.uuid4()),
        status=random.choice(statuses),
        name=random.choice(order_names)
    )

@app.get("/user", response_model=User)
def get_user() -> User:
    return User(
        id=str(uuid.uuid4()),
        username=random.choice(usernames)
    )

@app.get("/catalog", response_model=List[Product])
def get_catalog() -> List[Product]:
    return [Product(**item) for item in CATALOG]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
