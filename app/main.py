"""
app/main.py
FastAPI entry point for the Agentic Trading system.
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from datetime import datetime, timezone

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

import database.models as _models  # noqa: F401 — registers tables with SQLModel metadata
from database.connection import get_session, init_db


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Startup: create DB tables. Shutdown: nothing special yet."""
    await init_db()
    yield


app = FastAPI(
    title="Agentic Trading API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)) -> dict:
    """Prove the API and database are alive."""
    try:
        await session.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "db": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "db": str(exc),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )
