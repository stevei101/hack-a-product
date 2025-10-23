#!/usr/bin/env python3
"""
Test script to verify backend setup.
"""

import sys
import os

# Set up environment variables for development
os.environ["SECRET_KEY"] = "dev-secret-key-for-testing-only"
os.environ["API_KEY"] = "dev-api-key-for-testing-only"
os.environ["POSTGRES_PASSWORD"] = "dev-password"
os.environ["NIM_API_KEY"] = "dev-nim-key"
os.environ["LOG_LEVEL"] = "INFO"

# Add the backend src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

try:
    print("🧪 Testing Backend Setup...")
    print("=" * 50)
    
    # Test 1: Database setup
    print("\n1. Testing database setup...")
    from agentic_app.core.sync_database import Base, sync_engine, get_sync_db
    print("✅ Database setup successful")
    
    # Test 2: Models
    print("\n2. Testing models...")
    from agentic_app.models.project import Project, ChatMessage, Workflow, Idea, UserSettings
    print("✅ All models imported successfully")
    
    # Test 3: Services
    print("\n3. Testing services...")
    from agentic_app.services.ai_companion_service import ai_companion_service
    print("✅ AI Companion service imported successfully")
    
    # Test 4: API endpoints
    print("\n4. Testing API endpoints...")
    from agentic_app.api.v1.endpoints.projects import router as projects_router
    from agentic_app.api.v1.endpoints.ai_companion import router as ai_companion_router
    print("✅ API endpoints imported successfully")
    
    # Test 5: Create tables
    print("\n5. Creating database tables...")
    Base.metadata.create_all(bind=sync_engine)
    print("✅ Database tables created successfully")
    
    # Test 6: Main app
    print("\n6. Testing main app...")
    from agentic_app.main import app
    print("✅ Main app imported successfully")
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Backend is ready to start.")
    print("\n📋 Next steps:")
    print("   1. Run: make backend-dev")
    print("   2. Test: python test_enhanced_backend.py")
    print("   3. Frontend: make dev")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
