#!/usr/bin/env python3
"""
Simple test to check if the backend imports work.
"""

try:
    print("Testing backend imports...")
    
    # Test basic imports
    from agentic_app.models.project import Project, Idea, ChatMessage, Workflow, UserSettings
    print("✅ Project models imported successfully")
    
    from agentic_app.services.ai_companion_service import ai_companion_service
    print("✅ AI Companion service imported successfully")
    
    from agentic_app.api.v1.endpoints.projects import router as projects_router
    print("✅ Projects router imported successfully")
    
    from agentic_app.api.v1.endpoints.ai_companion import router as ai_companion_router
    print("✅ AI Companion router imported successfully")
    
    from agentic_app.main import app
    print("✅ Main app imported successfully")
    
    print("\n🎉 All imports successful! Backend should work.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
