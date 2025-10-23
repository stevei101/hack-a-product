"""OpenAI ChatGPT connector for MCP server."""

import httpx
import time
from typing import Any, Dict
from ..base_connector import BaseConnector
from ..models import ToolCapability, ToolInfo, ToolRequest, ToolResponse, ToolStatus


class OpenAIConnector(BaseConnector):
    """Connector for OpenAI ChatGPT."""
    
    def __init__(self, api_key: str):
        tool_info = ToolInfo(
            id="openai",
            name="OpenAI ChatGPT",
            description="OpenAI's ChatGPT for conversational AI and code generation",
            capabilities=[
                ToolCapability.TEXT_GENERATION,
                ToolCapability.CODE_GENERATION,
                ToolCapability.DATA_ANALYSIS,
                ToolCapability.TRANSLATION
            ],
            config={"api_key": api_key},
            rate_limit=60,  # requests per minute
            cost_per_request=0.002
        )
        super().__init__(tool_info)
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
    
    async def execute(self, request: ToolRequest) -> ToolResponse:
        """Execute an OpenAI request."""
        start_time = time.time()
        
        try:
            await self._apply_rate_limit()
            
            if not await self.validate_input(request.input_data):
                raise ValueError("Invalid input data")
            
            # Prepare OpenAI request
            messages = request.input_data.get("messages", [])
            model = request.parameters.get("model", "gpt-3.5-turbo")
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": request.parameters.get("temperature", 0.7),
                "max_tokens": request.parameters.get("max_tokens", 2048),
                "top_p": request.parameters.get("top_p", 1.0),
                "frequency_penalty": request.parameters.get("frequency_penalty", 0.0),
                "presence_penalty": request.parameters.get("presence_penalty", 0.0)
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                output_text = ""
                
                if "choices" in result and len(result["choices"]) > 0:
                    output_text = result["choices"][0]["message"]["content"]
                
                execution_time = time.time() - start_time
                
                return ToolResponse(
                    tool_id=self.tool_info.id,
                    success=True,
                    output_data={
                        "text": output_text,
                        "model": model,
                        "usage": result.get("usage", {})
                    },
                    execution_time=execution_time,
                    cost=self.tool_info.cost_per_request,
                    metadata={"model": model, "provider": "openai"}
                )
                
        except Exception as e:
            return await self._handle_error(e, request)
    
    async def health_check(self) -> bool:
        """Check OpenAI API health."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                return response.status_code == 200
        except Exception:
            return False
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate OpenAI input data."""
        return "messages" in input_data and isinstance(input_data["messages"], list)
