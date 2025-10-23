#!/usr/bin/env python3
"""Test script for MCP Server functionality."""

import asyncio
import httpx
import json
from typing import Dict, Any


async def test_mcp_server():
    """Test MCP server endpoints."""
    base_url = "http://localhost:8000/api/v1/mcp"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("🧪 Testing MCP Server...")
        
        # Test 1: Get available tools
        print("\n1. Testing GET /tools")
        try:
            response = await client.get(f"{base_url}/tools")
            if response.status_code == 200:
                tools = response.json()
                print(f"✅ Found {len(tools)} available tools:")
                for tool in tools:
                    print(f"   - {tool['name']} ({tool['id']})")
            else:
                print(f"❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 2: Get workflow templates
        print("\n2. Testing GET /workflows")
        try:
            response = await client.get(f"{base_url}/workflows")
            if response.status_code == 200:
                workflows = response.json()
                print(f"✅ Found {len(workflows)} workflow templates:")
                for workflow in workflows:
                    print(f"   - {workflow['name']} ({workflow['id']})")
            else:
                print(f"❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 3: Health check
        print("\n3. Testing GET /health")
        try:
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                health = response.json()
                print("✅ Health check results:")
                for tool_id, status in health.items():
                    status_icon = "✅" if status else "❌"
                    print(f"   {status_icon} {tool_id}: {'Healthy' if status else 'Unhealthy'}")
            else:
                print(f"❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 4: Single tool execution (if Gemini is available)
        print("\n4. Testing single tool execution")
        try:
            test_request = {
                "tool_id": "gemini",
                "input_data": {
                    "prompt": "Hello, this is a test message. Please respond with 'MCP Server test successful!'"
                },
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 100
                }
            }
            
            response = await client.post(
                f"{base_url}/tools/execute",
                json=test_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Single tool execution successful:")
                print(f"   Tool: {result['tool_id']}")
                print(f"   Success: {result['success']}")
                print(f"   Execution time: {result['execution_time']:.2f}s")
                if result['success']:
                    print(f"   Output: {result['output_data'].get('text', 'No text output')[:100]}...")
                else:
                    print(f"   Error: {result['error_message']}")
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 5: Orchestration (if multiple tools are available)
        print("\n5. Testing orchestration")
        try:
            orchestration_request = {
                "workflow_id": "test_orchestration_123",
                "tools": ["gemini", "openai"],  # Try both if available
                "input_data": {
                    "prompt": "Generate a simple product idea",
                    "action": "ideate"
                },
                "strategy": "parallel",
                "max_parallel": 2,
                "timeout": 60,
                "context": {
                    "temperature": 0.7,
                    "max_tokens": 200
                }
            }
            
            response = await client.post(
                f"{base_url}/orchestrate",
                json=orchestration_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Orchestration successful:")
                print(f"   Workflow ID: {result['workflow_id']}")
                print(f"   Success: {result['success']}")
                print(f"   Tools executed: {len(result['results'])}")
                print(f"   Total execution time: {result['total_execution_time']:.2f}s")
                print(f"   Total cost: ${result['total_cost']:.4f}")
                
                for tool_result in result['results']:
                    status_icon = "✅" if tool_result['success'] else "❌"
                    print(f"   {status_icon} {tool_result['tool_id']}: {tool_result['execution_time']:.2f}s")
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n🎉 MCP Server testing completed!")


async def test_frontend_integration():
    """Test frontend integration endpoints."""
    print("\n🌐 Testing Frontend Integration...")
    
    # Test if the frontend is running
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:3000")
            if response.status_code == 200:
                print("✅ Frontend is running on http://localhost:3000")
            else:
                print(f"❌ Frontend not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend not running: {e}")


if __name__ == "__main__":
    print("🚀 MCP Server Test Suite")
    print("=" * 50)
    
    # Run tests
    asyncio.run(test_mcp_server())
    asyncio.run(test_frontend_integration())
    
    print("\n📋 Next Steps:")
    print("1. Ensure backend is running: make backend-dev")
    print("2. Ensure frontend is running: make dev")
    print("3. Add API keys to backend/.env file")
    print("4. Test individual tool connectors")
    print("5. Create custom workflow templates")
