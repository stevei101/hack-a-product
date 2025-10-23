import asyncio
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx
from pydantic import BaseModel

from agentic_app.core.config import settings
from agentic_app.mcp.server import mcp_server
from agentic_app.mcp.models import ToolRequest, ToolResponse, OrchestrationRequest


class AICompanionMessage(BaseModel):
    """AI Companion message model."""
    id: int
    project_id: Optional[int] = None
    message_type: str  # 'user' or 'ai'
    content: str
    timestamp: datetime
    ai_provider: Optional[str] = None
    model_version: Optional[str] = None
    tokens_used: Optional[int] = None
    tools_used: Optional[List[str]] = None
    tool_results: Optional[Dict[str, Any]] = None


class AICompanionRequest(BaseModel):
    """Request model for AI Companion interactions."""
    project_id: Optional[int] = None
    message: str
    ai_provider: str = "nvidia-nim"
    use_tools: bool = True
    context: Optional[Dict[str, Any]] = None


class AICompanionResponse(BaseModel):
    """Response model for AI Companion interactions."""
    message: AICompanionMessage
    suggested_tools: Optional[List[str]] = None
    tool_executions: Optional[List[Dict[str, Any]]] = None
    reasoning: Optional[str] = None


class AICompanionService:
    """Service for AI Companion interactions with tool usage."""
    
    def __init__(self):
        self.nemotron_endpoint = getattr(settings, 'NEMOTRON_ENDPOINT', 'http://localhost:8000/v1')
        self.nemotron_api_key = getattr(settings, 'NEMOTRON_API_KEY', '')
    
    async def process_message(self, request: AICompanionRequest) -> AICompanionResponse:
        """Process a user message and generate AI response with tool usage."""
        
        # Step 1: Analyze the message to determine if tools are needed
        tool_analysis = await self._analyze_message_for_tools(request.message)
        
        # Step 2: Execute tools if needed
        tool_executions = []
        tool_results = {}
        if request.use_tools and tool_analysis['needs_tools']:
            tool_executions = await self._execute_recommended_tools(
                request.message, 
                tool_analysis['recommended_tools'],
                request.project_id
            )
            tool_results = {exec['tool']: exec['result'] for exec in tool_executions}
        
        # Step 3: Generate AI response with tool context
        ai_response = await self._generate_ai_response(
            request.message,
            tool_results,
            request.ai_provider,
            request.context
        )
        
        # Step 4: Create response message
        response_message = AICompanionMessage(
            id=0,  # Will be set by database
            project_id=request.project_id,
            message_type='ai',
            content=ai_response['content'],
            timestamp=datetime.utcnow(),
            ai_provider=request.ai_provider,
            model_version=ai_response.get('model_version'),
            tokens_used=ai_response.get('tokens_used'),
            tools_used=[exec['tool'] for exec in tool_executions],
            tool_results=tool_results
        )
        
        return AICompanionResponse(
            message=response_message,
            suggested_tools=tool_analysis['recommended_tools'],
            tool_executions=tool_executions,
            reasoning=ai_response.get('reasoning')
        )
    
    async def _analyze_message_for_tools(self, message: str) -> Dict[str, Any]:
        """Analyze user message to determine which tools might be helpful."""
        
        # Simple keyword-based tool recommendation (can be enhanced with ML)
        recommended_tools = []
        message_lower = message.lower()
        
        # Tool recommendation logic
        if any(word in message_lower for word in ['search', 'find', 'look up', 'research']):
            recommended_tools.append('web_search')
        
        if any(word in message_lower for word in ['code', 'programming', 'script', 'function']):
            recommended_tools.append('code_generation')
        
        if any(word in message_lower for word in ['design', 'ui', 'mockup', 'wireframe']):
            recommended_tools.append('figma')
        
        if any(word in message_lower for word in ['github', 'repository', 'commit', 'pull request']):
            recommended_tools.append('github')
        
        if any(word in message_lower for word in ['document', 'write', 'content', 'blog']):
            recommended_tools.append('document_generation')
        
        if any(word in message_lower for word in ['analyze', 'data', 'chart', 'graph']):
            recommended_tools.append('data_analysis')
        
        return {
            'needs_tools': len(recommended_tools) > 0,
            'recommended_tools': recommended_tools,
            'confidence': 0.8 if recommended_tools else 0.2
        }
    
    async def _execute_recommended_tools(
        self, 
        message: str, 
        recommended_tools: List[str],
        project_id: Optional[int]
    ) -> List[Dict[str, Any]]:
        """Execute recommended tools and return results."""
        
        executions = []
        
        for tool_name in recommended_tools:
            try:
                # Map tool names to MCP tool IDs
                tool_mapping = {
                    'web_search': 'gemini',
                    'code_generation': 'openai',
                    'figma': 'figma',
                    'github': 'github',
                    'document_generation': 'openai',
                    'data_analysis': 'openai'
                }
                
                mcp_tool_id = tool_mapping.get(tool_name)
                if not mcp_tool_id:
                    continue
                
                # Create tool request
                tool_request = ToolRequest(
                    tool_id=mcp_tool_id,
                    parameters={
                        'query': message,
                        'project_id': project_id,
                        'context': f"AI Companion request: {message}"
                    }
                )
                
                # Execute tool via MCP server
                tool_response = await mcp_server.execute_tool(tool_request)
                
                executions.append({
                    'tool': tool_name,
                    'mcp_tool_id': mcp_tool_id,
                    'status': 'success' if tool_response.success else 'failed',
                    'result': tool_response.result,
                    'execution_time': tool_response.execution_time,
                    'error': tool_response.error
                })
                
            except Exception as e:
                executions.append({
                    'tool': tool_name,
                    'status': 'error',
                    'error': str(e),
                    'result': None
                })
        
        return executions
    
    async def _generate_ai_response(
        self,
        user_message: str,
        tool_results: Dict[str, Any],
        ai_provider: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate AI response using the specified provider."""
        
        if ai_provider == "nvidia-nim":
            return await self._generate_nemotron_response(user_message, tool_results, context)
        elif ai_provider == "aws-bedrock":
            return await self._generate_bedrock_response(user_message, tool_results, context)
        else:
            return await self._generate_openai_response(user_message, tool_results, context)
    
    async def _generate_nemotron_response(
        self,
        user_message: str,
        tool_results: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate response using NVIDIA Nemotron Nano."""
        
        # Build context with tool results
        system_prompt = """You are an AI Companion for "The Product Mindset" - an AI-powered ideation and design companion. 
        You help users with product ideation, planning, design, and execution using various tools and AI capabilities.
        
        You have access to tools and can use them to provide more helpful responses. When you use tools, 
        incorporate the results naturally into your response."""
        
        if tool_results:
            tool_context = "\n\nTool Results:\n"
            for tool, result in tool_results.items():
                tool_context += f"- {tool}: {result}\n"
            system_prompt += tool_context
        
        if context:
            context_str = f"\n\nProject Context: {json.dumps(context, indent=2)}"
            system_prompt += context_str
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.nemotron_endpoint}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.nemotron_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "nemotron-nano-8b",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        "max_tokens": 1000,
                        "temperature": 0.7
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        'content': data['choices'][0]['message']['content'],
                        'model_version': 'nemotron-nano-8b',
                        'tokens_used': data.get('usage', {}).get('total_tokens', 0),
                        'reasoning': f"Used Nemotron Nano with {len(tool_results)} tool results"
                    }
                else:
                    return {
                        'content': f"I apologize, but I'm having trouble connecting to the AI service right now. Here's what I can tell you: {user_message}",
                        'model_version': 'nemotron-nano-8b',
                        'tokens_used': 0,
                        'reasoning': f"Nemotron API error: {response.status_code}"
                    }
        
        except Exception as e:
            return {
                'content': f"I'm here to help! While I'm having some technical difficulties, I can still assist you with: {user_message}",
                'model_version': 'nemotron-nano-8b',
                'tokens_used': 0,
                'reasoning': f"Nemotron connection error: {str(e)}"
            }
    
    async def _generate_bedrock_response(
        self,
        user_message: str,
        tool_results: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate response using AWS Bedrock (Claude)."""
        # Placeholder for Bedrock integration
        return {
            'content': f"Using AWS Bedrock Claude: {user_message}",
            'model_version': 'claude-3-sonnet',
            'tokens_used': 0,
            'reasoning': "Bedrock integration pending"
        }
    
    async def _generate_openai_response(
        self,
        user_message: str,
        tool_results: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate response using OpenAI ChatGPT."""
        # Placeholder for OpenAI integration
        return {
            'content': f"Using OpenAI ChatGPT: {user_message}",
            'model_version': 'gpt-4',
            'tokens_used': 0,
            'reasoning': "OpenAI integration pending"
        }
    
    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools for the AI Companion."""
        try:
            tools = mcp_server.get_available_tools()
            return [
                {
                    'id': tool.id,
                    'name': tool.name,
                    'description': tool.description,
                    'status': tool.status,
                    'capabilities': tool.capabilities
                }
                for tool in tools
            ]
        except Exception as e:
            return []
    
    async def suggest_tools_for_message(self, message: str) -> List[str]:
        """Suggest tools that might be helpful for a given message."""
        analysis = await self._analyze_message_for_tools(message)
        return analysis['recommended_tools']


# Global instance
ai_companion_service = AICompanionService()
