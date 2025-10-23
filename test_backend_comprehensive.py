#!/usr/bin/env python3
"""
Comprehensive backend test script.
"""

import requests
import json

def test_backend_endpoints():
    """Test all backend endpoints."""
    base_url = "http://localhost:8003"
    
    print("🧪 Testing Backend Endpoints...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint: OK")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    print()
    
    # Test MCP tools endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/mcp/tools", timeout=5)
        if response.status_code == 200:
            print("✅ MCP Tools endpoint: OK")
            tools_data = response.json()
            print(f"   Response type: {type(tools_data)}")
            print(f"   Response: {json.dumps(tools_data, indent=2)}")
        else:
            print(f"❌ MCP Tools endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ MCP Tools endpoint error: {e}")
    
    print()
    
    # Test MCP health endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/mcp/health", timeout=5)
        if response.status_code == 200:
            print("✅ MCP Health endpoint: OK")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ MCP Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ MCP Health endpoint error: {e}")
    
    print()
    
    # Test projects endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/projects", timeout=5)
        if response.status_code == 200:
            print("✅ Projects endpoint: OK")
            projects_data = response.json()
            print(f"   Projects count: {len(projects_data)}")
        else:
            print(f"❌ Projects endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Projects endpoint error: {e}")
    
    print()
    
    # Test API documentation
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API Documentation: Available")
            print(f"   URL: {base_url}/docs")
        else:
            print(f"❌ API Documentation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API Documentation error: {e}")

if __name__ == "__main__":
    test_backend_endpoints()
