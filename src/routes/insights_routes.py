from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.models.insights_models import Overview, Category, TopRatedBook, PriceRangeBook
from typing import List

from src.service.insights_service import overview_statistics, get_categories_insights, get_top_rated_books, get_price_range


router_insights = APIRouter(prefix="/insights")

@router_insights.get("/v1/stats/overview", response_model = Overview)
async def get_insights_overview():
    return overview_statistics()

@router_insights.get("/v1/stats/categories", response_model=List[Category])
async def get_insights_categories():
    return get_categories_insights()

@router_insights.get("/v1/stats/top-rated", response_model=List[TopRatedBook])
async def get_insights_top_rated():
    return get_top_rated_books()

@router_insights.get("/v1/stats/price-range/{min_price}/{max_price}", response_model=List[PriceRangeBook])
async def get_insights_price_range(min_price: float, max_price: float):
    return get_price_range(min_price, max_price)