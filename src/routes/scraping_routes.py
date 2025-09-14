# src/routers/scraping_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.service.web_scraping_service import Scraper

router_scraping = APIRouter(prefix="/scraping")


# Modelo para receber URL de forma validada
class ScrapingRequest(BaseModel):
    url: str


@router_scraping.post("/v1/update_bd")
async def update_bd(request: ScrapingRequest):
    """
    Extrai todos os livros de um site e atualiza a base de dados.
    """
    try:

        scraper = Scraper(base_url=request.url)

        print(scraper.base_url)
        
        books = scraper.scrape_all_books()
        
        return {"message": "Books tables updated successfully!", "books_count": len(books)}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update books")
