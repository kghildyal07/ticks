from fastapi import APIRouter

from app.v1.ticks.views import ticks_router
from app.v1.statistics.views import stats_router


api_router = APIRouter()

api_router.include_router(ticks_router, prefix="/ticks", tags=["ticks"])
api_router.include_router(stats_router, prefix="/statistics", tags=["statistics"])
