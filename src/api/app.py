from fastapi import FastAPI
from src.routes.scraping_routes import router_scraping  
from src.routes.book_routes import router_books  
from src.routes.insights_routes import router_insights  
from src.routes.auth_routes import router_auth  
from src.routes.health_routes import router_health

"""
Arquivo responsável pela organização das rotas da API
"""


def create_app():
    app = FastAPI(title="FIAP Projeto Fase 1", version="1.0.0")

    app.include_router(
        router_auth,
        prefix="/api",   
        tags=["Auth"],
    )

    app.include_router(
        router_health,
        prefix="/api",
        tags=["Health"],
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
