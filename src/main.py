from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from .database.connection import Base, engine
from .routers import events_aggregator, events_provider, system


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(events_provider.router)
app.include_router(events_aggregator.router)
app.include_router(system.router)


@app.exception_handler(Exception)
async def http_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    error = {
        "result": False,
        "error_type": exc.__class__.__name__,
        "error_message": exc.__str__(),
    }
    return JSONResponse(content=error)
