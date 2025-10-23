"""MCP Server main implementation."""

import logging
from typing import Dict, List, Optional
from fastapi import HTTPException
from pydantic import BaseModel

from .models import (
    ToolInfo, 
    ToolRequest, 
    ToolResponse, 
    OrchestrationRequest, 
    OrchestrationResponse,
    WorkflowTemplate
)
from .orchestrator import OrchestrationEngine
from .connectors import (
    GeminiConnector,
    FigmaConnector,
    OpenAIConnector,
    GitHubConnector,
    CursorConnector
)
from ..core.config import settings

logger = logging.getLogger(__name__)


class MCPServer:
    """Main MCP Server implementation."""
    
    def __init__(self):
        self.orchestrator = OrchestrationEngine()
        self._initialized = False
    
    def _ensure_initialized(self):
        """Ensure MCP server is initialized."""
        if not self._initialized:
            self._initialize_tools()
            self._initialize_workflow_templates()
            self._initialized = True
    
    def _initialize_tools(self) -> None:
        """Initialize all available tool connectors."""
        try:
            # Initialize Gemini
            if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
                gemini = GeminiConnector(settings.GEMINI_API_KEY)
                self.orchestrator.register_tool(gemini)
            
            # Initialize Figma
            if hasattr(settings, 'FIGMA_API_KEY') and settings.FIGMA_API_KEY:
                figma = FigmaConnector(settings.FIGMA_API_KEY)
                self.orchestrator.register_tool(figma)
            
            # Initialize OpenAI
            if hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
                openai = OpenAIConnector(settings.OPENAI_API_KEY)
                self.orchestrator.register_tool(openai)
            
            # Initialize GitHub
            if hasattr(settings, 'GITHUB_ACCESS_TOKEN') and settings.GITHUB_ACCESS_TOKEN:
                github = GitHubConnector(settings.GITHUB_ACCESS_TOKEN)
                self.orchestrator.register_tool(github)
            
            # Initialize Cursor
            if hasattr(settings, 'CURSOR_API_KEY') and settings.CURSOR_API_KEY:
                cursor = CursorConnector(settings.CURSOR_API_KEY)
                self.orchestrator.register_tool(cursor)
            
            logger.info(f"Initialized {len(self.orchestrator.tools)} tools")
            
        except Exception as e:
            logger.error(f"Failed to initialize tools: {e}")
    
    def _initialize_workflow_templates(self) -> None:
        """Initialize common workflow templates."""
        templates = [
            WorkflowTemplate(
                id="ideation_workflow",
                name="AI Ideation Workflow",
                description="Generate ideas using multiple AI tools",
                tools=["gemini", "openai"],
                parameters={"temperature": 0.8, "max_tokens": 2048},
                strategy="parallel"
            ),
            WorkflowTemplate(
                id="design_workflow",
                name="Design & Code Workflow",
                description="Design with Figma and generate code",
                tools=["figma", "cursor", "github"],
                parameters={"format": "png", "language": "typescript"},
                strategy="hybrid"
            ),
            WorkflowTemplate(
                id="code_review_workflow",
                name="Code Review Workflow",
                description="Review code using multiple AI tools",
                tools=["openai", "cursor", "github"],
                parameters={"temperature": 0.3, "max_tokens": 1024},
                strategy="sequential"
            ),
            WorkflowTemplate(
                id="research_workflow",
                name="Research Workflow",
                description="Research topics using multiple sources",
                tools=["gemini", "openai", "github"],
                parameters={"temperature": 0.7, "max_tokens": 4096},
                strategy="parallel"
            )
        ]
        
        for template in templates:
            self.orchestrator.register_workflow_template(template)
        
        logger.info(f"Initialized {len(templates)} workflow templates")
    
    async def execute_tool(self, request: ToolRequest) -> ToolResponse:
        """Execute a single tool."""
        self._ensure_initialized()
        if request.tool_id not in self.orchestrator.tools:
            raise HTTPException(status_code=404, detail=f"Tool {request.tool_id} not found")
        
        tool = self.orchestrator.tools[request.tool_id]
        
        if tool.get_status().value != "available":
            raise HTTPException(status_code=503, detail=f"Tool {request.tool_id} is not available")
        
        try:
            return await tool.execute(request)
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def execute_orchestration(self, request: OrchestrationRequest) -> OrchestrationResponse:
        """Execute orchestration with multiple tools."""
        self._ensure_initialized()
        try:
            return await self.orchestrator.execute_orchestration(request)
        except Exception as e:
            logger.error(f"Orchestration failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_available_tools(self) -> List[ToolInfo]:
        """Get list of available tools."""
        self._ensure_initialized()
        return [tool.tool_info for tool in self.orchestrator.tools.values()]
    
    def get_tool_info(self, tool_id: str) -> Optional[ToolInfo]:
        """Get information about a specific tool."""
        self._ensure_initialized()
        if tool_id in self.orchestrator.tools:
            return self.orchestrator.tools[tool_id].tool_info
        return None
    
    def get_workflow_templates(self) -> List[WorkflowTemplate]:
        """Get available workflow templates."""
        self._ensure_initialized()
        return self.orchestrator.list_workflow_templates()
    
    def get_workflow_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        """Get a specific workflow template."""
        self._ensure_initialized()
        return self.orchestrator.get_workflow_template(template_id)
    
    async def health_check(self) -> Dict[str, bool]:
        """Check health of all tools."""
        self._ensure_initialized()
        return await self.orchestrator.health_check_all_tools()
    
    def register_custom_tool(self, tool_id: str, connector) -> None:
        """Register a custom tool connector."""
        self.orchestrator.register_tool(connector)
        logger.info(f"Registered custom tool: {tool_id}")
    
    def unregister_tool(self, tool_id: str) -> None:
        """Unregister a tool."""
        self.orchestrator.unregister_tool(tool_id)
        logger.info(f"Unregistered tool: {tool_id}")


# Global MCP Server instance
mcp_server = MCPServer()
