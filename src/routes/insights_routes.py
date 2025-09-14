from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.service.insights_service import overview_statistics


router_insights = APIRouter(prefix="/insights")

@router_insights.get("/v1/overview")
async def get_insights_overview():
    return overview_statistics()