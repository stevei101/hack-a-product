"""Cursor editor connector for MCP server."""

import httpx
import time
from typing import Any, Dict
from ..base_connector import BaseConnector
from ..models import ToolCapability, ToolInfo, ToolRequest, ToolResponse, ToolStatus


class CursorConnector(BaseConnector):
    """Connector for Cursor AI code editor."""
    
    def __init__(self, api_key: str):
        tool_info = ToolInfo(
            id="cursor",
            name="Cursor AI",
            description="AI-powered code editor with intelligent code completion",
            capabilities=[
                ToolCapability.CODE_GENERATION,
                ToolCapability.TEXT_GENERATION
            ],
            config={"api_key": api_key},
            rate_limit=100,  # requests per minute
            cost_per_request=0.001
        )
        super().__init__(tool_info)
        self.api_key = api_key
        self.base_url = "https://api.cursor.sh/v1"
    
    async def execute(self, request: ToolRequest) -> ToolResponse:
        """Execute a Cursor request."""
        start_time = time.time()
        
        try:
            await self._apply_rate_limit()
            
            if not await self.validate_input(request.input_data):
                raise ValueError("Invalid input data")
            
            # Prepare Cursor request
            prompt = request.input_data.get("prompt", "")
            code_context = request.input_data.get("code_context", "")
            language = request.parameters.get("language", "typescript")
            
            payload = {
                "prompt": prompt,
                "code_context": code_context,
                "language": language,
                "temperature": request.parameters.get("temperature", 0.7),
                "max_tokens": request.parameters.get("max_tokens", 2048)
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                output_code = result.get("completion", "")
                
                execution_time = time.time() - start_time
                
                return ToolResponse(
                    tool_id=self.tool_info.id,
                    success=True,
                    output_data={
                        "completion": output_code,
                        "language": language,
                        "context": code_context
                    },
                    execution_time=execution_time,
                    cost=self.tool_info.cost_per_request,
                    metadata={"language": language, "provider": "cursor"}
                )
                
        except Exception as e:
            return await self._handle_error(e, request)
    
    async def health_check(self) -> bool:
        """Check Cursor API health."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/health",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                return response.status_code == 200
        except Exception:
            return False
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate Cursor input data."""
        return "prompt" in input_data and isinstance(input_data["prompt"], str)
