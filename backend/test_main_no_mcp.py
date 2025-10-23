"""Test main app without MCP server initialization."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agentic_app.core.config import settings
from agentic_app.core.logging import configure_logging

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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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

@app.get("/test-mcp")
async def test_mcp():
    """Test MCP server initialization."""
    try:
        from agentic_app.mcp.server import mcp_server
        tools = mcp_server.get_available_tools()
        return {"status": "success", "tools": len(tools)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
