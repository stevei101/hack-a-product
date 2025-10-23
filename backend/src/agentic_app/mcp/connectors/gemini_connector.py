"""Google Gemini connector for MCP server."""

import httpx
import time
from typing import Any, Dict
from ..base_connector import BaseConnector
from ..models import ToolCapability, ToolInfo, ToolRequest, ToolResponse, ToolStatus


class GeminiConnector(BaseConnector):
    """Connector for Google Gemini AI."""
    
    def __init__(self, api_key: str):
        tool_info = ToolInfo(
            id="gemini",
            name="Google Gemini",
            description="Google's advanced AI model for text generation and analysis",
            capabilities=[
                ToolCapability.TEXT_GENERATION,
                ToolCapability.CODE_GENERATION,
                ToolCapability.DATA_ANALYSIS,
                ToolCapability.TRANSLATION
            ],
            config={"api_key": api_key},
            rate_limit=60,  # requests per minute
            cost_per_request=0.001
        )
        super().__init__(tool_info)
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    async def execute(self, request: ToolRequest) -> ToolResponse:
        """Execute a Gemini request."""
        start_time = time.time()
        
        try:
            await self._apply_rate_limit()
            
            if not await self.validate_input(request.input_data):
                raise ValueError("Invalid input data")
            
            # Prepare Gemini request
            prompt = request.input_data.get("prompt", "")
            model = request.parameters.get("model", "gemini-1.5-flash")
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": request.parameters.get("temperature", 0.7),
                    "topK": request.parameters.get("top_k", 40),
                    "topP": request.parameters.get("top_p", 0.95),
                    "maxOutputTokens": request.parameters.get("max_tokens", 2048)
                }
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/models/{model}:generateContent",
                    params={"key": self.api_key},
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                output_text = ""
                
                if "candidates" in result and len(result["candidates"]) > 0:
                    candidate = result["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        output_text = candidate["content"]["parts"][0].get("text", "")
                
                execution_time = time.time() - start_time
                
                return ToolResponse(
                    tool_id=self.tool_info.id,
                    success=True,
                    output_data={
                        "text": output_text,
                        "model": model,
                        "usage": result.get("usageMetadata", {})
                    },
                    execution_time=execution_time,
                    cost=self.tool_info.cost_per_request,
                    metadata={"model": model, "provider": "google"}
                )
                
        except Exception as e:
            return await self._handle_error(e, request)
    
    async def health_check(self) -> bool:
        """Check Gemini API health."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    params={"key": self.api_key}
                )
                return response.status_code == 200
        except Exception:
            return False
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate Gemini input data."""
        return "prompt" in input_data and isinstance(input_data["prompt"], str)
