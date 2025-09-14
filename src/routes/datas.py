from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.service.get_data import get_data_from_csv, get_data_by_id, get_data_by_category_title


router_books = APIRouter(prefix="/books")


@router_books.get("/v1/books")
async def get_data():
    """
    Extract data from a website based on the specified url and update the books database.
    Args:
        request (ScrapingCategory): The request body containing the URL, tag, and class name.
    Returns:
        Message indicating the success of the operation.
    """
    

    try:
        
        books = get_data_from_csv("./src/data/books_data.csv")

        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_books.get("/v1/books/{book_id}")
async def get_book_by_id(book_id: int):
    """
    Retrieve a specific book record by its ID.
    Args:
        book_id (int): The ID of the book to retrieve.
    Returns:
        dict: The book record with the specified ID, or an error message if not found.
    """
    try:
        

        book = get_data_by_id("./src/data/books_data.csv", book_id)

        if book:
            return book
        else:
            raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_books.get("/v1/books/search/")
async def get_book_by_title_category(title: Optional[str] = None, category: Optional[str] = None):
    """
    Retrieve books by title and category.
    Args:
        title (str): The title of the book to search for.
        category (str): The category of the book to search for.
    Returns:
        list: A list of books matching the title and category, or an error message if none found.
    """
    try:

        books = get_data_by_category_title("./src/data/books_data.csv", category, title)

        if books:
            return books
        else:
            raise HTTPException(status_code=404, detail=f"No books found with title '{title}' in category '{category}'.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_books.get("/v1/health")
async def health_check():
    """
    Health check endpoint to verify that the service is running.
    Returns:
        dict: A message indicating that the service is healthy.
    """

    try:
        book = get_data_from_csv("./src/data/books_data.csv")

        return {
            "status": "OK",
            "code": 200,
            "message": "API is running and data is accessible.",
            "records_count": len(book)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))