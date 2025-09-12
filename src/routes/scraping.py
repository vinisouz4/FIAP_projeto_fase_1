from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from src.service.web_scraping import scrape_service


router_scraping = APIRouter(prefix="/scraping")

class ScrapingRequest(BaseModel):

    """Request model for web scraping.
    Attributes:
        url (str): The URL of the website to scrape.
        tag (str): The HTML tag to search for.
        class_name (str): The class name of the HTML elements to search for."""

    url: str
    tag: str
    class_name: str
    pages: int = 1  # Número de páginas a serem raspadas, padrão é 1


@router_scraping.post("/v1/extract")
async def extract_data(request: ScrapingRequest):
    """
    Extract data from a website based on the specified tag and class name.
    Args:
        request (ScrapingRequest): The request body containing the URL, tag, and class name.
    Returns:
        dict: A dictionary containing the extracted data.
    """
    

    try:
        
        data = scrape_service(
            request.url, 
            request.tag, 
            request.class_name,
            request.pages
        )
        
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))