"""Figma connector for MCP server."""

import httpx
import time
from typing import Any, Dict
from ..base_connector import BaseConnector
from ..models import ToolCapability, ToolInfo, ToolRequest, ToolResponse, ToolStatus


class FigmaConnector(BaseConnector):
    """Connector for Figma API."""
    
    def __init__(self, api_key: str):
        tool_info = ToolInfo(
            id="figma",
            name="Figma",
            description="Design collaboration platform for UI/UX design",
            capabilities=[
                ToolCapability.DESIGN_ASSISTANCE,
                ToolCapability.IMAGE_GENERATION
            ],
            config={"api_key": api_key},
            rate_limit=100,  # requests per minute
            cost_per_request=0.0  # Free tier
        )
        super().__init__(tool_info)
        self.access_token = api_key
        self.base_url = "https://api.figma.com/v1"
    
    async def execute(self, request: ToolRequest) -> ToolResponse:
        """Execute a Figma request."""
        start_time = time.time()
        
        try:
            await self._apply_rate_limit()
            
            if not await self.validate_input(request.input_data):
                raise ValueError("Invalid input data")
            
            action = request.input_data.get("action", "get_file")
            file_key = request.input_data.get("file_key", "")
            
            headers = {
                "X-Figma-Token": self.access_token,
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                if action == "get_file":
                    response = await client.get(
                        f"{self.base_url}/files/{file_key}",
                        headers=headers
                    )
                elif action == "get_images":
                    node_ids = request.input_data.get("node_ids", [])
                    format_type = request.parameters.get("format", "png")
                    scale = request.parameters.get("scale", 1)
                    
                    response = await client.get(
                        f"{self.base_url}/images/{file_key}",
                        headers=headers,
                        params={
                            "ids": ",".join(node_ids),
                            "format": format_type,
                            "scale": scale
                        }
                    )
                elif action == "get_comments":
                    response = await client.get(
                        f"{self.base_url}/files/{file_key}/comments",
                        headers=headers
                    )
                else:
                    raise ValueError(f"Unsupported action: {action}")
                
                response.raise_for_status()
                result = response.json()
                
                execution_time = time.time() - start_time
                
                return ToolResponse(
                    tool_id=self.tool_info.id,
                    success=True,
                    output_data=result,
                    execution_time=execution_time,
                    cost=self.tool_info.cost_per_request,
                    metadata={"action": action, "provider": "figma"}
                )
                
        except Exception as e:
            return await self._handle_error(e, request)
    
    async def health_check(self) -> bool:
        """Check Figma API health."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/me",
                    headers={"X-Figma-Token": self.access_token}
                )
                return response.status_code == 200
        except Exception:
            return False
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate Figma input data."""
        required_fields = ["action"]
        return all(field in input_data for field in required_fields)
