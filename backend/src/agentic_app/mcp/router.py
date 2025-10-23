"""MCP Server API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from .server import mcp_server
from .models import (
    ToolRequest, 
    ToolResponse, 
    OrchestrationRequest, 
    OrchestrationResponse,
    ToolInfo,
    WorkflowTemplate
)

router = APIRouter(prefix="/mcp", tags=["MCP Server"])


class ToolExecutionRequest(BaseModel):
    """Request model for tool execution."""
    tool_id: str
    input_data: dict
    parameters: dict = {}
    context: dict = {}
    priority: int = 1


class OrchestrationExecutionRequest(BaseModel):
    """Request model for orchestration execution."""
    workflow_id: str
    tools: List[str]
    input_data: dict
    strategy: str = "parallel"
    max_parallel: int = 3
    timeout: int = 300
    context: dict = {}


@router.get("/tools", response_model=List[ToolInfo])
async def get_available_tools():
    """Get list of available tools."""
    return mcp_server.get_available_tools()


@router.get("/tools/{tool_id}", response_model=ToolInfo)
async def get_tool_info(tool_id: str):
    """Get information about a specific tool."""
    tool_info = mcp_server.get_tool_info(tool_id)
    if not tool_info:
        raise HTTPException(status_code=404, detail=f"Tool {tool_id} not found")
    return tool_info


@router.post("/tools/execute", response_model=ToolResponse)
async def execute_tool(request: ToolExecutionRequest):
    """Execute a single tool."""
    tool_request = ToolRequest(
        tool_id=request.tool_id,
        input_data=request.input_data,
        parameters=request.parameters,
        context=request.context,
        priority=request.priority
    )
    
    return await mcp_server.execute_tool(tool_request)


@router.post("/orchestrate", response_model=OrchestrationResponse)
async def execute_orchestration(request: OrchestrationExecutionRequest):
    """Execute orchestration with multiple tools."""
    orchestration_request = OrchestrationRequest(
        workflow_id=request.workflow_id,
        tools=request.tools,
        input_data=request.input_data,
        strategy=request.strategy,
        max_parallel=request.max_parallel,
        timeout=request.timeout,
        context=request.context
    )
    
    return await mcp_server.execute_orchestration(orchestration_request)


@router.get("/workflows", response_model=List[WorkflowTemplate])
async def get_workflow_templates():
    """Get available workflow templates."""
    return mcp_server.get_workflow_templates()


@router.get("/workflows/{template_id}", response_model=WorkflowTemplate)
async def get_workflow_template(template_id: str):
    """Get a specific workflow template."""
    template = mcp_server.get_workflow_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail=f"Workflow template {template_id} not found")
    return template


@router.get("/health")
async def health_check():
    """Check health of all tools."""
    return await mcp_server.health_check()


@router.post("/workflows/{template_id}/execute", response_model=OrchestrationResponse)
async def execute_workflow_template(
    template_id: str,
    input_data: dict,
    context: dict = {}
):
    """Execute a workflow template."""
    template = mcp_server.get_workflow_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail=f"Workflow template {template_id} not found")
    
    # Merge template parameters with provided context
    merged_context = {**template.parameters, **context}
    
    orchestration_request = OrchestrationRequest(
        workflow_id=f"{template_id}_{hash(str(input_data))}",
        tools=template.tools,
        input_data=input_data,
        strategy=template.strategy,
        context=merged_context
    )
    
    return await mcp_server.execute_orchestration(orchestration_request)
