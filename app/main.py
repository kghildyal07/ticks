from fastapi import FastAPI
from contextlib import asynccontextmanager


from app.api import api_router
from app.utils.tick_manager import TickManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize the lifespan context manager
    """
    print("Initializing Tick Manager...")

    # Create and initialize a TickManager instance
    tick_manager = TickManager()
    app.state.tick_manager = tick_manager

    # Yield control back to FastAPI (this point means the app is running)
    yield

    # Clean up resources on shutdown
    print("Cleaning up the caches...")
    tick_manager.clear()


app = FastAPI(title="Ticks Rest Service", version="0.0.1", lifespan=lifespan)

app.include_router(api_router, prefix="/v1")
