#!/usr/bin/env python3
"""
Test script for the enhanced backend with AI Companion and Project Management.
"""

import asyncio
import httpx
import json
from datetime import datetime


async def test_backend_endpoints():
    """Test the new backend endpoints."""
    base_url = "http://localhost:8002/api/v1"
    
    async with httpx.AsyncClient() as client:
        print("🚀 Testing Enhanced Backend with AI Companion & Project Management")
        print("=" * 70)
        
        # Test 1: Health check
        print("\n1. Testing Health Check...")
        try:
            response = await client.get("http://localhost:8002/health")
            print(f"✅ Health Check: {response.json()}")
        except Exception as e:
            print(f"❌ Health Check failed: {e}")
            return
        
        # Test 2: MCP Tools
        print("\n2. Testing MCP Tools...")
        try:
            response = await client.get(f"{base_url}/mcp/tools")
            tools = response.json()
            print(f"✅ MCP Tools: {len(tools.get('tools', []))} tools available")
            for tool in tools.get('tools', []):
                print(f"   - {tool['name']}: {tool['status']}")
        except Exception as e:
            print(f"❌ MCP Tools failed: {e}")
        
        # Test 3: Create a project
        print("\n3. Testing Project Creation...")
        try:
            project_data = {
                "name": "Test AI Project",
                "description": "Testing the AI Companion with tools",
                "ai_provider": "nvidia-nim",
                "settings": {"test_mode": True}
            }
            response = await client.post(f"{base_url}/projects/", json=project_data)
            project = response.json()
            project_id = project['id']
            print(f"✅ Project Created: {project['name']} (ID: {project_id})")
        except Exception as e:
            print(f"❌ Project Creation failed: {e}")
            project_id = None
        
        # Test 4: Get projects
        print("\n4. Testing Project List...")
        try:
            response = await client.get(f"{base_url}/projects/")
            projects = response.json()
            print(f"✅ Projects: {len(projects)} projects found")
            for proj in projects:
                print(f"   - {proj['name']}: {proj['status']}")
        except Exception as e:
            print(f"❌ Project List failed: {e}")
        
        # Test 5: AI Companion tools
        print("\n5. Testing AI Companion Tools...")
        try:
            response = await client.get(f"{base_url}/ai-companion/tools")
            tools = response.json()
            print(f"✅ AI Companion Tools: {len(tools)} tools available")
            for tool in tools:
                print(f"   - {tool['name']}: {tool['status']}")
        except Exception as e:
            print(f"❌ AI Companion Tools failed: {e}")
        
        # Test 6: Tool suggestion
        print("\n6. Testing Tool Suggestion...")
        try:
            test_message = "I need help with coding a React component"
            response = await client.post(
                f"{base_url}/ai-companion/suggest-tools",
                params={"message": test_message}
            )
            suggestion = response.json()
            print(f"✅ Tool Suggestion for '{test_message}':")
            print(f"   Suggested tools: {suggestion['suggested_tools']}")
            print(f"   Reasoning: {suggestion['reasoning']}")
        except Exception as e:
            print(f"❌ Tool Suggestion failed: {e}")
        
        # Test 7: AI Companion chat (if project was created)
        if project_id:
            print("\n7. Testing AI Companion Chat...")
            try:
                chat_data = {
                    "project_id": project_id,
                    "message": "Hello! Can you help me brainstorm ideas for a mobile app?",
                    "ai_provider": "nvidia-nim",
                    "use_tools": True
                }
                response = await client.post(f"{base_url}/ai-companion/chat", json=chat_data)
                chat_response = response.json()
                print(f"✅ AI Companion Chat:")
                print(f"   AI Response: {chat_response['message']['content'][:100]}...")
                if chat_response.get('suggested_tools'):
                    print(f"   Suggested Tools: {chat_response['suggested_tools']}")
                if chat_response.get('tool_executions'):
                    print(f"   Tool Executions: {len(chat_response['tool_executions'])}")
            except Exception as e:
                print(f"❌ AI Companion Chat failed: {e}")
        
        # Test 8: Chat history (if project was created)
        if project_id:
            print("\n8. Testing Chat History...")
            try:
                response = await client.get(f"{base_url}/ai-companion/projects/{project_id}/chat-history")
                history = response.json()
                print(f"✅ Chat History: {len(history['messages'])} messages")
                for msg in history['messages']:
                    print(f"   - {msg['message_type']}: {msg['content'][:50]}...")
            except Exception as e:
                print(f"❌ Chat History failed: {e}")
        
        print("\n" + "=" * 70)
        print("🎉 Backend testing completed!")
        print("\n📋 Available Endpoints:")
        print("   - GET  /health")
        print("   - GET  /api/v1/mcp/tools")
        print("   - GET  /api/v1/projects/")
        print("   - POST /api/v1/projects/")
        print("   - GET  /api/v1/ai-companion/tools")
        print("   - POST /api/v1/ai-companion/chat")
        print("   - POST /api/v1/ai-companion/suggest-tools")
        print("   - GET  /api/v1/ai-companion/projects/{id}/chat-history")


if __name__ == "__main__":
    asyncio.run(test_backend_endpoints())
