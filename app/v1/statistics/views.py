from fastapi import APIRouter, Request

from app.v1.statistics.schemas import Stats

stats_router = APIRouter()


# GET /statistics endpoint
@stats_router.get("/")
async def get_stats_service(request: Request) -> Stats:
    tick_manager = request.app.state.tick_manager
    return await tick_manager.get_all_stats()


# GET /statistics/{instrument_identifier} endpoint
@stats_router.get("/{instrument_identifier}")
async def get_instrument_statistics(
    instrument_identifier: str, request: Request
) -> Stats:
    tick_manager = request.app.state.tick_manager
    return await tick_manager.get_instrument_stats(instrument_identifier)
