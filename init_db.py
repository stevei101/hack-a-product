#!/usr/bin/env python3
"""
Initialize the SQLite database with all tables.
"""

from agentic_app.core.sync_database import sync_engine, Base
from agentic_app.models.project import Project, ChatMessage, Workflow, Idea, UserSettings

def create_tables():
    """Create all database tables."""
    try:
        # Import all models to ensure they're registered with Base
        Base.metadata.create_all(bind=sync_engine)
        print("✅ Database tables created successfully!")
        print("📁 SQLite database: agentic_app.db")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()
