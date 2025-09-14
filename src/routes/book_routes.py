from fastapi import APIRouter, HTTPException
from typing import Optional, List

from src.service.book_service import get_all_books, get_book_id, search_books
from src.models.book_models import Book, HealthResponse



router_books = APIRouter(prefix="/books")


@router_books.get("/v1/books", response_model=List[Book])
async def get_books():
    """
    Extract data from a website based on the specified url and update the books database.
    Args:
        request (ScrapingCategory): The request body containing the URL, tag, and class name.
    Returns:
        Message indicating the success of the operation.
    """
    

    try:

        books = get_all_books()

        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_books.get("/v1/books/{book_id}", response_model=Book)
async def get_book_by_id(book_id: str):
    """
    Retrieve a specific book record by its ID.
    Args:
        book_id (str): The ID of the book to retrieve.
    Returns:
        dict: The book record with the specified ID, or an error message if not found.
    """
    try:
        

        book = get_book_id(book_id)

        if not book:
            raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
        return book
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_books.get("/v1/books/search/", response_model=List[Book])
async def search(title: Optional[str] = None, category: Optional[str] = None):
    try:
        books = search_books(title, category)
        if not books:
            raise HTTPException(status_code=404, detail="No books found")
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router_books.get("/v1/health", response_model=HealthResponse)
async def health_check():
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