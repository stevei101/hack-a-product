#!/usr/bin/env python3
"""Comprehensive test script for MCP server."""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

async def test_mcp_server():
    """Test the MCP server functionality."""
    try:
        print("🚀 Testing MCP Server...")
        
        # Import MCP components
        from agentic_app.mcp.server import mcp_server
        from agentic_app.mcp.models import ToolRequest, OrchestrationRequest
        
        print("✅ MCP Server imported successfully!")
        
        # Test 1: Get available tools
        print("\n📋 Test 1: Getting available tools...")
        tools = mcp_server.get_available_tools()
        print(f"Found {len(tools)} available tools:")
        for tool in tools:
            print(f"  - {tool.id}: {tool.name} ({tool.status})")
        
        # Test 2: Get workflow templates
        print("\n📋 Test 2: Getting workflow templates...")
        templates = mcp_server.get_workflow_templates()
        print(f"Found {len(templates)} workflow templates:")
        for template in templates:
            print(f"  - {template.id}: {template.name}")
            print(f"    Tools: {template.tools}")
            print(f"    Strategy: {template.strategy}")
        
        # Test 3: Health check
        print("\n📋 Test 3: Health check...")
        health_status = await mcp_server.health_check()
        print("Tool health status:")
        for tool_id, is_healthy in health_status.items():
            status = "✅ Healthy" if is_healthy else "❌ Unhealthy"
            print(f"  - {tool_id}: {status}")
        
        # Test 4: Test single tool execution (if tools are available)
        if tools:
            print("\n📋 Test 4: Testing single tool execution...")
            tool_id = tools[0].id
            print(f"Testing tool: {tool_id}")
            
            # Create a test request
            test_request = ToolRequest(
                tool_id=tool_id,
                input_data={"prompt": "Hello, this is a test!"},
                parameters={"temperature": 0.7},
                context={"test": True}
            )
            
            try:
                response = await mcp_server.execute_tool(test_request)
                if response.success:
                    print(f"✅ Tool execution successful!")
                    print(f"   Execution time: {response.execution_time:.2f}s")
                    print(f"   Cost: ${response.cost:.4f}")
                else:
                    print(f"❌ Tool execution failed: {response.error_message}")
            except Exception as e:
                print(f"⚠️  Tool execution error (expected if no API keys): {e}")
        
        # Test 5: Test orchestration (if multiple tools available)
        if len(tools) > 1:
            print("\n📋 Test 5: Testing orchestration...")
            tool_ids = [tool.id for tool in tools[:2]]  # Use first 2 tools
            
            orchestration_request = OrchestrationRequest(
                workflow_id="test_workflow",
                tools=tool_ids,
                input_data={"prompt": "Test orchestration"},
                strategy="parallel",
                max_parallel=2,
                timeout=30
            )
            
            try:
                response = await mcp_server.execute_orchestration(orchestration_request)
                print(f"✅ Orchestration completed!")
                print(f"   Success: {response.success}")
                print(f"   Total execution time: {response.total_execution_time:.2f}s")
                print(f"   Total cost: ${response.total_cost:.4f}")
                print(f"   Results: {len(response.results)} tool responses")
            except Exception as e:
                print(f"⚠️  Orchestration error (expected if no API keys): {e}")
        
        print("\n🎉 MCP Server testing completed!")
        print("\n📝 Summary:")
        print(f"  - Tools available: {len(tools)}")
        print(f"  - Workflow templates: {len(templates)}")
        print(f"  - Health checks: {len(health_status)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mcp_server())
    sys.exit(0 if success else 1)
