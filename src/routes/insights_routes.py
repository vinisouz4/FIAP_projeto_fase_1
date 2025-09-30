from fastapi import APIRouter, Depends
from src.models.insights_models import Overview, Category, TopRatedBook, PriceRangeBook, BestValueBook, CategoryByPrice
from typing import List
from src.service.auth_service import current_user


from src.service.insights_service import overview_statistics, get_categories_insights, get_top_rated_books, get_price_range, get_best_value, get_group_by_price

user_dependency = Depends(current_user)

router_insights = APIRouter(prefix="/insights")

@router_insights.get("/v1/stats/overview", response_model = Overview)
async def get_insights_overview(user: str = user_dependency):
    try:
        overview = overview_statistics()
        return overview
    except Exception as e:
        return {"error": str(e)}

@router_insights.get("/v1/stats/categories", response_model=List[Category])
async def get_insights_categories(user: str = user_dependency):
    try:
        categories = get_categories_insights()
        return categories
    except Exception as e:
        return {"error": str(e)}

@router_insights.get("/v1/stats/top-rated", response_model=List[TopRatedBook])
async def get_insights_top_rated(user: str = user_dependency):
    try:
        top_rated = get_top_rated_books()
        return top_rated
    except Exception as e:
        return {"error": str(e)}

@router_insights.get("/v1/stats/price-range/{min_price}/{max_price}", response_model=List[PriceRangeBook])
async def get_insights_price_range(min_price: float, max_price: float, user: str = user_dependency):
    try:
        return get_price_range(min_price, max_price)
    except Exception as e:
        return {"error": str(e)}
    
@router_insights.get("/v1/stats/best-value", response_model=List[BestValueBook])
async def get_insights_best_value(user: str = user_dependency):
    try:
        return get_best_value()
    except Exception as e:
        return {"error": str(e)}
    
@router_insights.get("/v1/stats/count-by-group-price", response_model=List[CategoryByPrice])
async def get_count_group_by_price(user: str = user_dependency):
    try:
        return get_group_by_price()
    except Exception as e:
        return {"error": str(e)}