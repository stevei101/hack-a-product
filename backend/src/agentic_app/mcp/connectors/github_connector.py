"""GitHub Copilot connector for MCP server."""

import httpx
import time
from typing import Any, Dict
from ..base_connector import BaseConnector
from ..models import ToolCapability, ToolInfo, ToolRequest, ToolResponse, ToolStatus


class GitHubConnector(BaseConnector):
    """Connector for GitHub API and Copilot."""
    
    def __init__(self, access_token: str):
        tool_info = ToolInfo(
            id="github",
            name="GitHub Copilot",
            description="GitHub's AI-powered code completion and generation",
            capabilities=[
                ToolCapability.CODE_GENERATION,
                ToolCapability.SEARCH
            ],
            config={"access_token": access_token},
            rate_limit=5000,  # requests per hour
            cost_per_request=0.0  # Free tier
        )
        super().__init__(tool_info)
        self.access_token = access_token
        self.base_url = "https://api.github.com"
    
    async def execute(self, request: ToolRequest) -> ToolResponse:
        """Execute a GitHub request."""
        start_time = time.time()
        
        try:
            await self._apply_rate_limit()
            
            if not await self.validate_input(request.input_data):
                raise ValueError("Invalid input data")
            
            action = request.input_data.get("action", "search_repositories")
            
            headers = {
                "Authorization": f"token {self.access_token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "MCP-Server"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                if action == "search_repositories":
                    query = request.input_data.get("query", "")
                    response = await client.get(
                        f"{self.base_url}/search/repositories",
                        headers=headers,
                        params={"q": query}
                    )
                elif action == "get_repository":
                    owner = request.input_data.get("owner", "")
                    repo = request.input_data.get("repo", "")
                    response = await client.get(
                        f"{self.base_url}/repos/{owner}/{repo}",
                        headers=headers
                    )
                elif action == "get_file_contents":
                    owner = request.input_data.get("owner", "")
                    repo = request.input_data.get("repo", "")
                    path = request.input_data.get("path", "")
                    response = await client.get(
                        f"{self.base_url}/repos/{owner}/{repo}/contents/{path}",
                        headers=headers
                    )
                elif action == "get_issues":
                    owner = request.input_data.get("owner", "")
                    repo = request.input_data.get("repo", "")
                    response = await client.get(
                        f"{self.base_url}/repos/{owner}/{repo}/issues",
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
                    metadata={"action": action, "provider": "github"}
                )
                
        except Exception as e:
            return await self._handle_error(e, request)
    
    async def health_check(self) -> bool:
        """Check GitHub API health."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/user",
                    headers={"Authorization": f"token {self.access_token}"}
                )
                return response.status_code == 200
        except Exception:
            return False
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate GitHub input data."""
        required_fields = ["action"]
        return all(field in input_data for field in required_fields)
