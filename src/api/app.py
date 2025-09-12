from fastapi import FastAPI
from src.routes.scraping import router_scraping  # importa o router de scraping

def create_app():
    app = FastAPI(title="FIAP Projeto Fase 1", version="1.0.0")

    # Inclui o roteador de scraping com prefixo e tags
    app.include_router(
        router_scraping,
        prefix="/api",   # prefixo geral
        tags=["API"],   # tags extras
    )

    return app
