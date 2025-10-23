// MCP Server API client for frontend
export interface ToolInfo {
  id: string;
  name: string;
  description: string;
  capabilities: string[];
  status: string;
  config: Record<string, any>;
  rate_limit?: number;
  cost_per_request?: number;
}

export interface ToolResponse {
  tool_id: string;
  success: boolean;
  output_data: Record<string, any>;
  error_message?: string;
  execution_time: number;
  cost?: number;
  metadata: Record<string, any>;
}

export interface OrchestrationResponse {
  workflow_id: string;
  success: boolean;
  results: ToolResponse[];
  aggregated_output: Record<string, any>;
  total_execution_time: number;
  total_cost?: number;
  errors: string[];
}

export interface WorkflowTemplate {
  id: string;
  name: string;
  description: string;
  tools: string[];
  parameters: Record<string, any>;
  strategy: string;
}

class MCPServerClient {
  private baseUrl: string;

  constructor(baseUrl: string = 'http://localhost:8002/api/v1') {
    this.baseUrl = baseUrl;
  }

  async getAvailableTools(): Promise<ToolInfo[]> {
    const response = await fetch(`${this.baseUrl}/mcp/tools`);
    if (!response.ok) {
      throw new Error(`Failed to fetch tools: ${response.statusText}`);
    }
    return response.json();
  }

  async getToolInfo(toolId: string): Promise<ToolInfo> {
    const response = await fetch(`${this.baseUrl}/mcp/tools/${toolId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch tool info: ${response.statusText}`);
    }
    return response.json();
  }

  async executeTool(toolId: string, inputData: Record<string, any>, parameters: Record<string, any> = {}): Promise<ToolResponse> {
    const response = await fetch(`${this.baseUrl}/mcp/tools/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        tool_id: toolId,
        input_data: inputData,
        parameters,
        context: {},
        priority: 1
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to execute tool: ${response.statusText}`);
    }
    return response.json();
  }

  async executeOrchestration(
    workflowId: string,
    tools: string[],
    inputData: Record<string, any>,
    strategy: string = 'parallel',
    maxParallel: number = 3,
    timeout: number = 300
  ): Promise<OrchestrationResponse> {
    const response = await fetch(`${this.baseUrl}/mcp/orchestrate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        workflow_id: workflowId,
        tools,
        input_data: inputData,
        strategy,
        max_parallel: maxParallel,
        timeout,
        context: {}
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to execute orchestration: ${response.statusText}`);
    }
    return response.json();
  }

  async getWorkflowTemplates(): Promise<WorkflowTemplate[]> {
    const response = await fetch(`${this.baseUrl}/mcp/workflows`);
    if (!response.ok) {
      throw new Error(`Failed to fetch workflow templates: ${response.statusText}`);
    }
    return response.json();
  }

  async getWorkflowTemplate(templateId: string): Promise<WorkflowTemplate> {
    const response = await fetch(`${this.baseUrl}/mcp/workflows/${templateId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch workflow template: ${response.statusText}`);
    }
    return response.json();
  }

  async executeWorkflowTemplate(templateId: string, inputData: Record<string, any>, context: Record<string, any> = {}): Promise<OrchestrationResponse> {
    const response = await fetch(`${this.baseUrl}/mcp/workflows/${templateId}/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        input_data: inputData,
        context
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to execute workflow template: ${response.statusText}`);
    }
    return response.json();
  }

  async healthCheck(): Promise<Record<string, boolean>> {
    const response = await fetch(`${this.baseUrl}/mcp/health`);
    if (!response.ok) {
      throw new Error(`Failed to check health: ${response.statusText}`);
    }
    return response.json();
  }
}

export default MCPServerClient;
