"""Synchronous database configuration for compatibility."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from agentic_app.core.config import settings

# Use SQLite for development to avoid psycopg2 dependency
DATABASE_URL = "sqlite:///./agentic_app.db"

# Create Base for models
Base = declarative_base()

# Create synchronous engine
sync_engine = create_engine(
    DATABASE_URL,
    echo=settings.LOG_LEVEL == "DEBUG",
    connect_args={"check_same_thread": False}  # SQLite specific
)

# Create synchronous session factory
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


def get_sync_db() -> Session:
    """Get synchronous database session."""
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
