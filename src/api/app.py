from fastapi import FastAPI
from src.routes.scraping import router_scraping  # importa o router de scraping
from src.routes.datas import router_books  # importa o router de books
from src.routes.insights import router_insights  # importa o router de insights

def create_app():
    app = FastAPI(title="FIAP Projeto Fase 1", version="1.0.0")

    # Inclui o roteador de scraping com prefixo e tags
    app.include_router(
        router_scraping,
        prefix="/api",   # prefixo geral
        tags=["API"],   # tags extras
    )

    app.include_router(
        router_books,
        prefix="/api",   # prefixo geral
        tags=["Books"],   # tags extras
    )

    app.include_router(
        router_insights,
        prefix="/api",   # prefixo geral
        tags=["Insights"],   # tags extras
    )

    return app
