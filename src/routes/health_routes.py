from fastapi import APIRouter, HTTPException, Depends

from src.service.book_service import get_all_books
from src.models.book_models import HealthResponse
from src.service.auth_service import current_user


router_health = APIRouter(prefix="/health")

user_dependency = Depends(current_user)


@router_health.get("/v1/health", response_model=HealthResponse)
async def health_check(user: str = user_dependency):
    try:
        books = get_all_books()
        return HealthResponse(
            status="OK",
            code=200,
            message="API is running and data is accessible.",
            records_count=len(books)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))