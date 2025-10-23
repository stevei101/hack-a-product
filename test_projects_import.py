#!/usr/bin/env python3
"""
Test script to check projects.py for syntax errors.
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
    print("🧪 Testing projects.py import...")
    print("=" * 50)
    
    # Test importing projects module
    from agentic_app.api.v1.endpoints import projects
    print("✅ projects.py imported successfully!")
    
    # Test importing the router
    router = projects.router
    print(f"✅ Router created with {len(router.routes)} routes")
    
    # List the routes
    for route in router.routes:
        print(f"  - {route.methods} {route.path}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except SyntaxError as e:
    print(f"❌ Syntax error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
    import traceback
    traceback.print_exc()
