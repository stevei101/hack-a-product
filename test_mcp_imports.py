#!/usr/bin/env python3
"""Test script to verify MCP server is working."""

import sys
import os
import asyncio

# Add the backend src directory to Python path
backend_src = os.path.join(os.path.dirname(__file__), 'backend', 'src')
sys.path.insert(0, backend_src)

def test_imports():
    """Test that all MCP components can be imported."""
    try:
        print("🔍 Testing MCP imports...")
        
        # Test core imports
        from agentic_app.mcp.models import ToolInfo, ToolRequest, OrchestrationRequest
        print("✅ MCP models imported successfully")
        
        from agentic_app.mcp.base_connector import BaseConnector
        print("✅ Base connector imported successfully")
        
        from agentic_app.mcp.orchestrator import OrchestrationEngine
        print("✅ Orchestration engine imported successfully")
        
        from agentic_app.mcp.server import MCPServer
        print("✅ MCP server imported successfully")
        
        from agentic_app.mcp.router import router
        print("✅ MCP router imported successfully")
        
        # Test connector imports
        from agentic_app.mcp.connectors import (
            GeminiConnector,
            FigmaConnector,
            OpenAIConnector,
            GitHubConnector,
            CursorConnector
        )
        print("✅ All tool connectors imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_mcp_server():
    """Test MCP server functionality."""
    try:
        print("\n🚀 Testing MCP server functionality...")
        
        from agentic_app.mcp.server import mcp_server
        
        # Test getting tools
        tools = mcp_server.get_available_tools()
        print(f"✅ Found {len(tools)} available tools")
        
        # Test getting workflow templates
        templates = mcp_server.get_workflow_templates()
        print(f"✅ Found {len(templates)} workflow templates")
        
        # Test health check
        health_status = await mcp_server.health_check()
        print(f"✅ Health check completed for {len(health_status)} tools")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP server test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fastapi_integration():
    """Test FastAPI integration."""
    try:
        print("\n🌐 Testing FastAPI integration...")
        
        from agentic_app.main import app
        print("✅ FastAPI app created successfully")
        
        # Check if MCP router is included
        routes = [route.path for route in app.routes]
        mcp_routes = [route for route in routes if '/mcp' in route]
        print(f"✅ Found {len(mcp_routes)} MCP routes: {mcp_routes}")
        
        return True
        
    except Exception as e:
        print(f"❌ FastAPI integration error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests."""
    print("🧪 MCP Server Test Suite")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    if not imports_ok:
        print("\n❌ Import tests failed. Check dependencies.")
        return False
    
    # Test MCP server
    mcp_ok = await test_mcp_server()
    if not mcp_ok:
        print("\n❌ MCP server tests failed.")
        return False
    
    # Test FastAPI integration
    fastapi_ok = test_fastapi_integration()
    if not fastapi_ok:
        print("\n❌ FastAPI integration tests failed.")
        return False
    
    print("\n🎉 All tests passed! MCP server is ready to use.")
    print("\n📝 Next steps:")
    print("  1. Run 'make backend-setup' to fix the Python environment")
    print("  2. Run 'make backend-dev' to start the server")
    print("  3. Run 'make dev' to start the frontend")
    print("  4. Visit http://localhost:3000 to test the MCP integration")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
