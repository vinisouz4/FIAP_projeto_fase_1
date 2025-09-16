from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: str               
    title: str
    price: float
    stock: str
    category: str
    rating: int

class Category(BaseModel):
    category: str

class HealthResponse(BaseModel):
    status: str
    code: int
    message: str
    records_count: int
