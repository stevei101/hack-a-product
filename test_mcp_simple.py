#!/usr/bin/env python3
"""Simple test script for MCP server."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

try:
    from agentic_app.mcp.server import mcp_server
    print("✅ MCP Server imported successfully!")
    
    # Test getting available tools
    tools = mcp_server.get_available_tools()
    print(f"✅ Found {len(tools)} available tools:")
    for tool in tools:
        print(f"  - {tool.id}: {tool.name} ({tool.status})")
    
    # Test workflow templates
    templates = mcp_server.get_workflow_templates()
    print(f"✅ Found {len(templates)} workflow templates:")
    for template in templates:
        print(f"  - {template.id}: {template.name}")
    
    print("\n🎉 MCP Server is working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
