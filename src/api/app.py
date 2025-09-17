from fastapi import FastAPI
from src.routes.scraping_routes import router_scraping  # importa o router de scraping
from src.routes.book_routes import router_books  # importa o router de books
from src.routes.insights_routes import router_insights  # importa o router de insights
from src.routes.auth_routes import router_auth  # importa o router de auth

def create_app():
    app = FastAPI(title="FIAP Projeto Fase 1", version="1.0.0")

    app.include_router(
        router_auth,
        prefix="/api",   
        tags=["Auth"],
    )

    app.include_router(
        router_scraping,
        prefix="/api",   
        tags=["Update Data"],   
    )

    app.include_router(
        router_books,
        prefix="/api",   
        tags=["Books"],   
    )

    app.include_router(
        router_insights,
        prefix="/api",   
        tags=["Insights"],   
    )

    return app
