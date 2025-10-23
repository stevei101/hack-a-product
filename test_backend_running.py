#!/usr/bin/env python3
"""
Simple test to check if backend is running.
"""

import requests
import time

def test_backend():
    """Test if backend is running."""
    try:
        # Wait a bit for backend to start
        time.sleep(3)
        
        # Test health endpoint
        response = requests.get("http://localhost:8003/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
            print(f"Health check: {response.json()}")
            
            # Test MCP tools endpoint
            try:
                tools_response = requests.get("http://localhost:8003/api/v1/mcp/tools", timeout=5)
                if tools_response.status_code == 200:
                    tools_data = tools_response.json()
                    print(f"✅ MCP Tools: {len(tools_data.get('tools', []))} tools available")
                else:
                    print(f"⚠️ MCP Tools endpoint returned: {tools_response.status_code}")
            except Exception as e:
                print(f"⚠️ MCP Tools test failed: {e}")
                
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running or not accessible")
    except Exception as e:
        print(f"❌ Error testing backend: {e}")

if __name__ == "__main__":
    test_backend()
