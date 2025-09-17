# src/routers/scraping_router.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel


from src.service.web_scraping_service import Scraper
from src.service.auth_service import current_user


router_scraping = APIRouter(prefix="/scraping")

user_dependency = Depends(current_user)


# Modelo para receber URL de forma validada
class ScrapingRequest(BaseModel):
    url: str


@router_scraping.post("/v1/update_bd")
async def update_bd(request: ScrapingRequest, user: str = user_dependency):
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
