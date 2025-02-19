import time
from fastapi import APIRouter, Request, Response

from app.v1.ticks.schemas import Ticks


ticks_router = APIRouter()


@ticks_router.post("/", status_code=201)
async def set_ticks(tick: Ticks, request: Request):
    now_ts = int(time.time() * 1000.0)
    if now_ts - tick.timestamp > 60000:
        return Response(status_code=204)

    tick_manager = request.app.state.tick_manager
    await tick_manager.add(tick)
    # Successfully added, status code 201 will be returned automatically
    return {}
