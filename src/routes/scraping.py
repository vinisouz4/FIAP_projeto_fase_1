from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from src.service.web_scraping import scrape_all_books, scrape_service_get_categories


router_scraping = APIRouter(prefix="/scraping")

class ScrapingCategory(BaseModel):
    url: str


@router_scraping.post("/v1/update_books_bd")
async def update_data(request: ScrapingCategory):
    """
    Extract data from a website based on the specified url and update the books database.
    Args:
        request (ScrapingCategory): The request body containing the URL, tag, and class name.
    Returns:
        Message indicating the success of the operation.
    """
    

    try:
        
        scrape_all_books(
            request.url
        )

        
        return {"Message": "Books tables updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router_scraping.post("/v1/update_categories")
async def update_categories(request: ScrapingCategory):
    """
    Extract categories from a website based on the specified tag and class name.
    Args:
        request (ScrapingRequest): The request body containing the URL, tag, and class name.
    Returns:
        dict: A dictionary containing the extracted categories.
    """
    try:
        scrape_service_get_categories(
            request.url
        )
        
        return {"message": "Categories extracted and saved successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))