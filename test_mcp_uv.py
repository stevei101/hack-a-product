#!/usr/bin/env python3
"""Simple MCP server test using uv."""

import asyncio
import sys
import os

# Add the backend src directory to Python path
backend_src = os.path.join(os.path.dirname(__file__), 'backend', 'src')
sys.path.insert(0, backend_src)

async def test_mcp():
    """Test MCP server functionality."""
    try:
        print("🚀 Testing MCP Server with uv...")
        
        # Import MCP components
        from agentic_app.mcp.server import mcp_server
        print("✅ MCP Server imported successfully!")
        
        # Test getting tools
        tools = mcp_server.get_available_tools()
        print(f"✅ Found {len(tools)} available tools:")
        for tool in tools:
            print(f"  - {tool.id}: {tool.name} ({tool.status})")
        
        # Test getting workflow templates
        templates = mcp_server.get_workflow_templates()
        print(f"✅ Found {len(templates)} workflow templates:")
        for template in templates:
            print(f"  - {template.id}: {template.name}")
            print(f"    Tools: {template.tools}")
            print(f"    Strategy: {template.strategy}")
        
        # Test health check
        health_status = await mcp_server.health_check()
        print(f"✅ Health check completed for {len(health_status)} tools:")
        for tool_id, is_healthy in health_status.items():
            status = "✅ Healthy" if is_healthy else "❌ Unhealthy"
            print(f"  - {tool_id}: {status}")
        
        print("\n🎉 MCP Server is working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mcp())
    sys.exit(0 if success else 1)
