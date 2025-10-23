"""MCP Orchestration Engine."""

import asyncio
import time
from typing import Any, Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor
import logging

from .models import (
    OrchestrationRequest, 
    OrchestrationResponse, 
    ToolRequest, 
    ToolResponse,
    WorkflowTemplate
)
from .base_connector import BaseConnector

logger = logging.getLogger(__name__)


class OrchestrationEngine:
    """Engine for orchestrating multiple tools."""
    
    def __init__(self):
        self.tools: Dict[str, BaseConnector] = {}
        self.workflow_templates: Dict[str, WorkflowTemplate] = {}
        self.executor = ThreadPoolExecutor(max_workers=10)
        
    def register_tool(self, connector: BaseConnector) -> None:
        """Register a tool connector."""
        self.tools[connector.tool_info.id] = connector
        logger.info(f"Registered tool: {connector.tool_info.name}")
    
    def unregister_tool(self, tool_id: str) -> None:
        """Unregister a tool connector."""
        if tool_id in self.tools:
            del self.tools[tool_id]
            logger.info(f"Unregistered tool: {tool_id}")
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool IDs."""
        return [tool_id for tool_id, tool in self.tools.items() 
                if tool.get_status().value == "available"]
    
    def register_workflow_template(self, template: WorkflowTemplate) -> None:
        """Register a workflow template."""
        self.workflow_templates[template.id] = template
        logger.info(f"Registered workflow template: {template.name}")
    
    async def execute_orchestration(self, request: OrchestrationRequest) -> OrchestrationResponse:
        """Execute orchestration with multiple tools."""
        start_time = time.time()
        results: List[ToolResponse] = []
        errors: List[str] = []
        
        try:
            # Validate tools are available
            unavailable_tools = []
            for tool_id in request.tools:
                if tool_id not in self.tools:
                    unavailable_tools.append(tool_id)
                elif self.tools[tool_id].get_status().value != "available":
                    unavailable_tools.append(tool_id)
            
            if unavailable_tools:
                raise ValueError(f"Unavailable tools: {unavailable_tools}")
            
            # Execute based on strategy
            if request.strategy == "parallel":
                results = await self._execute_parallel(request)
            elif request.strategy == "sequential":
                results = await self._execute_sequential(request)
            elif request.strategy == "hybrid":
                results = await self._execute_hybrid(request)
            else:
                raise ValueError(f"Unknown strategy: {request.strategy}")
            
            # Aggregate results
            aggregated_output = await self._aggregate_results(results)
            
            total_execution_time = time.time() - start_time
            total_cost = sum(r.cost or 0.0 for r in results)
            
            return OrchestrationResponse(
                workflow_id=request.workflow_id,
                success=len(errors) == 0,
                results=results,
                aggregated_output=aggregated_output,
                total_execution_time=total_execution_time,
                total_cost=total_cost,
                errors=errors
            )
            
        except Exception as e:
            logger.error(f"Orchestration failed: {e}")
            errors.append(str(e))
            
            return OrchestrationResponse(
                workflow_id=request.workflow_id,
                success=False,
                results=results,
                aggregated_output={},
                total_execution_time=time.time() - start_time,
                total_cost=0.0,
                errors=errors
            )
    
    async def _execute_parallel(self, request: OrchestrationRequest) -> List[ToolResponse]:
        """Execute tools in parallel."""
        tasks = []
        
        for tool_id in request.tools:
            tool_request = ToolRequest(
                tool_id=tool_id,
                input_data=request.input_data,
                parameters=request.context.get("parameters", {}),
                context=request.context,
                priority=request.context.get("priority", 1)
            )
            
            task = asyncio.create_task(
                self._execute_tool_with_timeout(tool_request, request.timeout)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(ToolResponse(
                    tool_id=request.tools[i],
                    success=False,
                    output_data={},
                    error_message=str(result),
                    execution_time=0.0,
                    cost=0.0
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _execute_sequential(self, request: OrchestrationRequest) -> List[ToolResponse]:
        """Execute tools sequentially."""
        results = []
        
        for tool_id in request.tools:
            tool_request = ToolRequest(
                tool_id=tool_id,
                input_data=request.input_data,
                parameters=request.context.get("parameters", {}),
                context=request.context,
                priority=request.context.get("priority", 1)
            )
            
            result = await self._execute_tool_with_timeout(tool_request, request.timeout)
            results.append(result)
            
            # Break on failure if configured
            if not result.success and request.context.get("stop_on_error", False):
                break
        
        return results
    
    async def _execute_hybrid(self, request: OrchestrationRequest) -> List[ToolResponse]:
        """Execute tools in hybrid mode (batches of parallel execution)."""
        results = []
        max_parallel = request.max_parallel
        
        # Split tools into batches
        tool_batches = [
            request.tools[i:i + max_parallel] 
            for i in range(0, len(request.tools), max_parallel)
        ]
        
        for batch in tool_batches:
            batch_request = OrchestrationRequest(
                workflow_id=f"{request.workflow_id}_batch_{len(results)}",
                tools=batch,
                input_data=request.input_data,
                strategy="parallel",
                max_parallel=max_parallel,
                timeout=request.timeout,
                context=request.context
            )
            
            batch_results = await self._execute_parallel(batch_request)
            results.extend(batch_results)
        
        return results
    
    async def _execute_tool_with_timeout(self, request: ToolRequest, timeout: int) -> ToolResponse:
        """Execute a tool with timeout."""
        try:
            return await asyncio.wait_for(
                self.tools[request.tool_id].execute(request),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            return ToolResponse(
                tool_id=request.tool_id,
                success=False,
                output_data={},
                error_message=f"Tool execution timed out after {timeout} seconds",
                execution_time=timeout,
                cost=0.0
            )
    
    async def _aggregate_results(self, results: List[ToolResponse]) -> Dict[str, Any]:
        """Aggregate results from multiple tools."""
        aggregated = {
            "total_tools": len(results),
            "successful_tools": len([r for r in results if r.success]),
            "failed_tools": len([r for r in results if not r.success]),
            "results_by_tool": {},
            "combined_output": {},
            "errors": []
        }
        
        for result in results:
            aggregated["results_by_tool"][result.tool_id] = {
                "success": result.success,
                "output": result.output_data,
                "execution_time": result.execution_time,
                "cost": result.cost,
                "error": result.error_message
            }
            
            if result.success:
                # Combine successful outputs
                if "text" in result.output_data:
                    aggregated["combined_output"]["text"] = aggregated["combined_output"].get("text", "") + "\n" + result.output_data["text"]
                if "completion" in result.output_data:
                    aggregated["combined_output"]["code"] = aggregated["combined_output"].get("code", "") + "\n" + result.output_data["completion"]
            else:
                aggregated["errors"].append(f"{result.tool_id}: {result.error_message}")
        
        return aggregated
    
    async def health_check_all_tools(self) -> Dict[str, bool]:
        """Check health of all registered tools."""
        health_status = {}
        
        for tool_id, tool in self.tools.items():
            try:
                health_status[tool_id] = await tool.health_check()
            except Exception as e:
                logger.error(f"Health check failed for {tool_id}: {e}")
                health_status[tool_id] = False
        
        return health_status
    
    def get_workflow_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        """Get a workflow template by ID."""
        return self.workflow_templates.get(template_id)
    
    def list_workflow_templates(self) -> List[WorkflowTemplate]:
        """List all available workflow templates."""
        return list(self.workflow_templates.values())
