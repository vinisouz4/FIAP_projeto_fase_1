from pydantic import BaseModel

class Overview(BaseModel):
    total_books: int       
    average_price: float
    rating_distribution: dict

class Category(BaseModel):
    category: str
    total_category: int
    average_price: float

class TopRatedBook(BaseModel):
    id: str
    title: str
    price: float
    rating: int
    category: str

class PriceRangeBook(BaseModel):
    id: str
    title: str
    price: float
    rating: int
    category: str