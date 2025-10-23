#!/usr/bin/env python3
"""Test if basic MCP server works without external dependencies."""

import asyncio
import sys
import os

# Add the backend src directory to Python path
backend_src = os.path.join(os.path.dirname(__file__), 'backend', 'src')
sys.path.insert(0, backend_src)

async def test_basic_mcp():
    """Test basic MCP server functionality."""
    try:
        print("🚀 Testing Basic MCP Server...")
        
        # Test core imports
        from agentic_app.mcp.models import ToolInfo, ToolRequest, OrchestrationRequest
        print("✅ MCP models imported successfully")
        
        from agentic_app.mcp.base_connector import BaseConnector
        print("✅ Base connector imported successfully")
        
        from agentic_app.mcp.orchestrator import OrchestrationEngine
        print("✅ Orchestration engine imported successfully")
        
        # Test server import
        from agentic_app.mcp.server import mcp_server
        print("✅ MCP server imported successfully")
        
        # Test getting tools (should work even without API keys)
        tools = mcp_server.get_available_tools()
        print(f"✅ Found {len(tools)} available tools")
        
        # Test getting workflow templates
        templates = mcp_server.get_workflow_templates()
        print(f"✅ Found {len(templates)} workflow templates:")
        for template in templates:
            print(f"  - {template.id}: {template.name}")
        
        # Test health check
        health_status = await mcp_server.health_check()
        print(f"✅ Health check completed for {len(health_status)} tools")
        
        print("\n🎉 Basic MCP Server is working!")
        print("💡 Note: Tools will show as unavailable without API keys, which is expected.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_basic_mcp())
    sys.exit(0 if success else 1)
