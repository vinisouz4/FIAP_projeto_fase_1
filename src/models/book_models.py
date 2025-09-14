from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: str               # agora é string UUID
    title: str
    price: float
    stock: str
    category: str
    rating: int

class HealthResponse(BaseModel):
    status: str
    code: int
    message: str
    records_count: int
