"""MCP Server data models."""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum


class ToolStatus(str, Enum):
    """Tool status enumeration."""
    AVAILABLE = "available"
    BUSY = "busy"
    ERROR = "error"
    UNAVAILABLE = "unavailable"


class ToolCapability(str, Enum):
    """Tool capability enumeration."""
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    DESIGN_ASSISTANCE = "design_assistance"
    IMAGE_GENERATION = "image_generation"
    DATA_ANALYSIS = "data_analysis"
    SEARCH = "search"
    TRANSLATION = "translation"


class ToolInfo(BaseModel):
    """Information about a registered tool."""
    id: str = Field(..., description="Unique tool identifier")
    name: str = Field(..., description="Human-readable tool name")
    description: str = Field(..., description="Tool description")
    capabilities: List[ToolCapability] = Field(..., description="Tool capabilities")
    status: ToolStatus = Field(default=ToolStatus.AVAILABLE, description="Current tool status")
    config: Dict[str, Any] = Field(default_factory=dict, description="Tool configuration")
    rate_limit: Optional[int] = Field(None, description="Rate limit per minute")
    cost_per_request: Optional[float] = Field(None, description="Cost per request in USD")


class ToolRequest(BaseModel):
    """Request to execute a tool."""
    tool_id: str = Field(..., description="Target tool identifier")
    input_data: Dict[str, Any] = Field(..., description="Input data for the tool")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Tool-specific parameters")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    priority: int = Field(default=1, description="Request priority (1-10)")


class ToolResponse(BaseModel):
    """Response from a tool execution."""
    tool_id: str = Field(..., description="Source tool identifier")
    success: bool = Field(..., description="Whether the execution was successful")
    output_data: Dict[str, Any] = Field(..., description="Output data from the tool")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    execution_time: float = Field(..., description="Execution time in seconds")
    cost: Optional[float] = Field(None, description="Cost of this request")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class OrchestrationRequest(BaseModel):
    """Request for multi-tool orchestration."""
    workflow_id: str = Field(..., description="Unique workflow identifier")
    tools: List[str] = Field(..., description="List of tool IDs to orchestrate")
    input_data: Dict[str, Any] = Field(..., description="Input data for the workflow")
    strategy: str = Field(default="parallel", description="Orchestration strategy: parallel, sequential, or hybrid")
    max_parallel: int = Field(default=3, description="Maximum parallel executions")
    timeout: int = Field(default=300, description="Timeout in seconds")
    context: Dict[str, Any] = Field(default_factory=dict, description="Workflow context")


class OrchestrationResponse(BaseModel):
    """Response from orchestration execution."""
    workflow_id: str = Field(..., description="Workflow identifier")
    success: bool = Field(..., description="Whether the orchestration was successful")
    results: List[ToolResponse] = Field(..., description="Results from all tools")
    aggregated_output: Dict[str, Any] = Field(..., description="Aggregated output")
    total_execution_time: float = Field(..., description="Total execution time")
    total_cost: Optional[float] = Field(None, description="Total cost")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")


class WorkflowTemplate(BaseModel):
    """Template for common workflows."""
    id: str = Field(..., description="Template identifier")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")
    tools: List[str] = Field(..., description="Required tools")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Default parameters")
    strategy: str = Field(default="parallel", description="Default strategy")
