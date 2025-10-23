"""Main FastAPI application for the Agentic Application."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agentic_app.core.config import settings
from agentic_app.core.logging import configure_logging
from agentic_app.mcp.router import router as mcp_router
from agentic_app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    configure_logging()
    logging.info("Agentic Application started successfully")
    
    yield
    
    # Shutdown
    logging.info("Agentic Application shutting down")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Agentic Application with NVIDIA NIM integration",
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    # Set up CORS
    cors_origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include MCP router
    app.include_router(mcp_router, prefix=settings.API_V1_STR)
    
    # Include API v1 router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_application()


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Agentic Application API", "version": "1.0.0"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/mcp/tools")
async def get_mcp_tools():
    """Get MCP tools (lazy initialization)."""
    try:
        from agentic_app.mcp.server import mcp_server
        tools = mcp_server.get_available_tools()
        return {"tools": [{"id": tool.id, "name": tool.name, "status": tool.status} for tool in tools]}
    except Exception as e:
        return {"error": str(e)}
