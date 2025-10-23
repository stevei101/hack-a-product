# MCP Server Implementation Guide

## Overview

The Model Context Protocol (MCP) Server provides a centralized orchestration layer for multiple AI tools and services. This implementation enables seamless integration with various AI providers and design tools, allowing users to orchestrate complex workflows across multiple platforms.

## Architecture

```
Frontend (React + TypeScript)
    ↓
MCP Server API (/api/v1/mcp/*)
    ↓
Orchestration Engine
    ↓
Tool Connectors (Gemini, Figma, ChatGPT, GitHub, Cursor)
    ↓
External APIs
```

## Features

### ✅ Implemented Features

1. **Multi-Tool Orchestration**
   - Parallel execution of multiple tools
   - Sequential execution for dependent workflows
   - Hybrid execution with configurable batching

2. **Tool Connectors**
   - Google Gemini (text generation, analysis)
   - Figma (design collaboration, file access)
   - OpenAI ChatGPT (conversational AI, code generation)
   - GitHub (repository access, code search)
   - Cursor AI (code completion, generation)

3. **Workflow Templates**
   - Pre-configured workflows for common tasks
   - Customizable parameters and strategies
   - Template-based execution

4. **Health Monitoring**
   - Real-time tool health checks
   - Status monitoring and error handling
   - Rate limiting and timeout management

5. **Frontend Integration**
   - Modern React UI matching the intended design
   - Tool selection interface
   - Real-time orchestration status
   - Action buttons for common workflows

## API Endpoints

### Tool Management
- `GET /api/v1/mcp/tools` - List available tools
- `GET /api/v1/mcp/tools/{tool_id}` - Get tool information
- `POST /api/v1/mcp/tools/execute` - Execute single tool

### Orchestration
- `POST /api/v1/mcp/orchestrate` - Execute multi-tool orchestration
- `GET /api/v1/mcp/workflows` - List workflow templates
- `GET /api/v1/mcp/workflows/{template_id}` - Get workflow template
- `POST /api/v1/mcp/workflows/{template_id}/execute` - Execute template

### Health & Monitoring
- `GET /api/v1/mcp/health` - Check all tool health status

## Configuration

### Environment Variables

Add these to your `backend/.env` file:

```bash
# MCP Server API Keys (Optional - tools will be disabled if not provided)
GEMINI_API_KEY=your_google_gemini_api_key_here
FIGMA_ACCESS_TOKEN=your_figma_access_token_here
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_ACCESS_TOKEN=your_github_access_token_here
CURSOR_API_KEY=your_cursor_api_key_here
```

### Getting API Keys

1. **Google Gemini**: Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Figma**: Generate access token from [Figma Account Settings](https://www.figma.com/settings)
3. **OpenAI**: Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
4. **GitHub**: Generate personal access token from [GitHub Settings](https://github.com/settings/tokens)
5. **Cursor**: Get API key from [Cursor AI Platform](https://cursor.sh)

## Usage Examples

### 1. Single Tool Execution

```typescript
const response = await fetch('/api/v1/mcp/tools/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    tool_id: 'gemini',
    input_data: {
      prompt: 'Generate a product idea for a mobile app'
    },
    parameters: {
      temperature: 0.8,
      max_tokens: 2048
    }
  })
});
```

### 2. Multi-Tool Orchestration

```typescript
const response = await fetch('/api/v1/mcp/orchestrate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    workflow_id: 'ideation_workflow_123',
    tools: ['gemini', 'openai', 'figma'],
    input_data: {
      prompt: 'Create a design for a productivity app',
      action: 'ideate'
    },
    strategy: 'parallel',
    max_parallel: 3,
    timeout: 300,
    context: {
      temperature: 0.7,
      max_tokens: 2048
    }
  })
});
```

### 3. Workflow Template Execution

```typescript
const response = await fetch('/api/v1/mcp/workflows/ideation_workflow/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    input_data: {
      prompt: 'Generate ideas for a sustainable product'
    },
    context: {
      temperature: 0.8
    }
  })
});
```

## Workflow Templates

### Available Templates

1. **Ideation Workflow**
   - Tools: Gemini, OpenAI
   - Strategy: Parallel
   - Purpose: Generate creative ideas using multiple AI models

2. **Design & Code Workflow**
   - Tools: Figma, Cursor, GitHub
   - Strategy: Hybrid
   - Purpose: Design interfaces and generate corresponding code

3. **Code Review Workflow**
   - Tools: OpenAI, Cursor, GitHub
   - Strategy: Sequential
   - Purpose: Review code using multiple perspectives

4. **Research Workflow**
   - Tools: Gemini, OpenAI, GitHub
   - Strategy: Parallel
   - Purpose: Research topics using multiple sources

## Frontend Integration

The frontend has been updated to match the intended "Product Mindset" design with:

- **Tool Selection Interface**: Choose which tools to orchestrate
- **Action Buttons**: Ideate, Plan, Design, Execute
- **Real-time Status**: Show orchestration progress
- **Results Display**: Aggregate outputs from all tools

### Key Components

- `App.tsx` - Main application with tool selection and orchestration
- Tool cards for AWS Bedrock and NVIDIA NIM
- MCP tool selection grid
- Agentic AI Architecture section with action buttons

## Error Handling

The MCP server includes comprehensive error handling:

- **Tool Unavailability**: Graceful degradation when tools are offline
- **Rate Limiting**: Automatic throttling to respect API limits
- **Timeout Management**: Configurable timeouts for long-running operations
- **Validation**: Input validation for all tool requests
- **Health Checks**: Regular monitoring of tool availability

## Performance Considerations

- **Parallel Execution**: Multiple tools can run simultaneously
- **Rate Limiting**: Built-in rate limiting per tool
- **Caching**: Tool responses can be cached for repeated requests
- **Timeout Management**: Prevents hanging requests
- **Resource Management**: Configurable concurrency limits

## Security

- **API Key Management**: Secure storage of external API keys
- **Input Validation**: All inputs are validated before processing
- **Rate Limiting**: Prevents abuse and ensures fair usage
- **Error Sanitization**: Sensitive information is not exposed in errors

## Monitoring & Logging

- **Health Checks**: Regular monitoring of all tool connectors
- **Structured Logging**: JSON-formatted logs for easy parsing
- **Metrics**: Execution time, success rates, and cost tracking
- **Error Tracking**: Comprehensive error logging and reporting

## Next Steps

1. **Test the Implementation**: Start the backend and test the MCP endpoints
2. **Configure API Keys**: Add your API keys to the environment file
3. **Customize Workflows**: Create custom workflow templates for your use cases
4. **Extend Tool Connectors**: Add new tools by implementing the BaseConnector interface
5. **Monitor Performance**: Use the health check endpoints to monitor tool availability

## Troubleshooting

### Common Issues

1. **Tool Not Available**: Check if the API key is correctly configured
2. **Rate Limit Exceeded**: Reduce parallel execution or increase rate limits
3. **Timeout Errors**: Increase timeout values for slow tools
4. **CORS Issues**: Ensure frontend URL is in BACKEND_CORS_ORIGINS

### Debug Mode

Enable debug logging by setting:
```bash
LOG_LEVEL=DEBUG
```

This will provide detailed information about tool execution and orchestration flow.
