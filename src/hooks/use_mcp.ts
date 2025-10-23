import { useState, useEffect, useCallback } from 'react';
import MCPServerClient, { ToolInfo, ToolResponse, OrchestrationResponse, WorkflowTemplate } from '../services/mcp_client';

export interface UseMCPReturn {
  // State
  tools: ToolInfo[];
  templates: WorkflowTemplate[];
  isLoading: boolean;
  error: string | null;
  healthStatus: Record<string, boolean>;

  // Actions
  executeTool: (toolId: string, inputData: Record<string, any>, parameters?: Record<string, any>) => Promise<ToolResponse>;
  executeOrchestration: (workflowId: string, tools: string[], inputData: Record<string, any>, strategy?: string) => Promise<OrchestrationResponse>;
  executeWorkflowTemplate: (templateId: string, inputData: Record<string, any>, context?: Record<string, any>) => Promise<OrchestrationResponse>;
  refreshTools: () => Promise<void>;
  refreshTemplates: () => Promise<void>;
  checkHealth: () => Promise<void>;
}

export function useMCP(baseUrl?: string): UseMCPReturn {
  const [mcpClient] = useState(() => new MCPServerClient(baseUrl));
  const [tools, setTools] = useState<ToolInfo[]>([]);
  const [templates, setTemplates] = useState<WorkflowTemplate[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [healthStatus, setHealthStatus] = useState<Record<string, boolean>>({});

  const refreshTools = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const availableTools = await mcpClient.getAvailableTools();
      setTools(availableTools);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch tools');
    } finally {
      setIsLoading(false);
    }
  }, [mcpClient]);

  const refreshTemplates = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const workflowTemplates = await mcpClient.getWorkflowTemplates();
      setTemplates(workflowTemplates);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch workflow templates');
    } finally {
      setIsLoading(false);
    }
  }, [mcpClient]);

  const checkHealth = useCallback(async () => {
    try {
      const health = await mcpClient.healthCheck();
      setHealthStatus(health);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to check health');
    }
  }, [mcpClient]);

  const executeTool = useCallback(async (
    toolId: string, 
    inputData: Record<string, any>, 
    parameters: Record<string, any> = {}
  ): Promise<ToolResponse> => {
    try {
      setError(null);
      return await mcpClient.executeTool(toolId, inputData, parameters);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to execute tool';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  }, [mcpClient]);

  const executeOrchestration = useCallback(async (
    workflowId: string,
    tools: string[],
    inputData: Record<string, any>,
    strategy: string = 'parallel'
  ): Promise<OrchestrationResponse> => {
    try {
      setError(null);
      return await mcpClient.executeOrchestration(workflowId, tools, inputData, strategy);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to execute orchestration';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  }, [mcpClient]);

  const executeWorkflowTemplate = useCallback(async (
    templateId: string,
    inputData: Record<string, any>,
    context: Record<string, any> = {}
  ): Promise<OrchestrationResponse> => {
    try {
      setError(null);
      return await mcpClient.executeWorkflowTemplate(templateId, inputData, context);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to execute workflow template';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  }, [mcpClient]);

  // Load initial data
  useEffect(() => {
    refreshTools();
    refreshTemplates();
    checkHealth();
  }, [refreshTools, refreshTemplates, checkHealth]);

  return {
    tools,
    templates,
    isLoading,
    error,
    healthStatus,
    executeTool,
    executeOrchestration,
    executeWorkflowTemplate,
    refreshTools,
    refreshTemplates,
    checkHealth,
  };
}
