"""Base connector interface for MCP tools."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import asyncio
import time
from ..mcp.models import ToolInfo, ToolRequest, ToolResponse, ToolStatus


class BaseConnector(ABC):
    """Base class for all tool connectors."""
    
    def __init__(self, tool_info: ToolInfo):
        self.tool_info = tool_info
        self._rate_limiter = None
        self._last_request_time = 0
        
    @abstractmethod
    async def execute(self, request: ToolRequest) -> ToolResponse:
        """Execute a request using this tool."""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the tool is healthy and available."""
        pass
    
    @abstractmethod
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for this tool."""
        pass
    
    async def _apply_rate_limit(self) -> None:
        """Apply rate limiting if configured."""
        if self.tool_info.rate_limit:
            current_time = time.time()
            time_since_last = current_time - self._last_request_time
            min_interval = 60.0 / self.tool_info.rate_limit
            
            if time_since_last < min_interval:
                await asyncio.sleep(min_interval - time_since_last)
            
            self._last_request_time = time.time()
    
    async def _handle_error(self, error: Exception, request: ToolRequest) -> ToolResponse:
        """Handle errors and return appropriate response."""
        self.tool_info.status = ToolStatus.ERROR
        
        return ToolResponse(
            tool_id=self.tool_info.id,
            success=False,
            output_data={},
            error_message=str(error),
            execution_time=0.0,
            cost=self.tool_info.cost_per_request or 0.0,
            metadata={"error_type": type(error).__name__}
        )
    
    def get_capabilities(self) -> list:
        """Get tool capabilities."""
        return self.tool_info.capabilities
    
    def get_status(self) -> ToolStatus:
        """Get current tool status."""
        return self.tool_info.status
    
    def update_status(self, status: ToolStatus) -> None:
        """Update tool status."""
        self.tool_info.status = status
