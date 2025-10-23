import { useState } from 'react';
import { Sparkles, Cloud, Cpu, Brain, Zap, Settings, HelpCircle } from 'lucide-react';

export default function App() {
  const [selectedTools, setSelectedTools] = useState<string[]>([]);
  const [isOrchestrating, setIsOrchestrating] = useState(false);

  const handleToolToggle = (toolId: string) => {
    setSelectedTools(prev => 
      prev.includes(toolId) 
        ? prev.filter(id => id !== toolId)
        : [...prev, toolId]
    );
  };

  const handleAction = async (action: string) => {
    if (selectedTools.length === 0) {
      alert('Please select at least one tool to orchestrate');
      return;
    }

    setIsOrchestrating(true);
    
    try {
      const response = await fetch('/api/v1/mcp/orchestrate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          workflow_id: `${action}_workflow_${Date.now()}`,
          tools: selectedTools,
          input_data: {
            action: action,
            prompt: `Please help me ${action.toLowerCase()} a new product idea`
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

      const result = await response.json();
      console.log('Orchestration result:', result);
      
      // Handle the result (you can display it in a modal or update UI)
      alert(`Orchestration completed! Used ${result.results.length} tools.`);
      
    } catch (error) {
      console.error('Orchestration failed:', error);
      alert('Orchestration failed. Please try again.');
    } finally {
      setIsOrchestrating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <Sparkles className="h-5 w-5 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">The Product Mindset</h1>
                  <p className="text-sm text-gray-500">AI-Powered Ideation & Design Companion</p>
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500">
                Built for the AWS & NVIDIA Hackathon
              </div>
              <button className="p-2 text-gray-400 hover:text-gray-600">
                <Settings className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            AI-Powered Ideation & Design Companion
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Orchestrate multiple AI tools to accelerate your product development process. 
            Choose your tools and let our MCP server coordinate the magic.
          </p>
        </div>

        {/* Tool Selection Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          {/* AWS Bedrock Card */}
          <div className="bg-white rounded-xl shadow-lg p-8 border-2 border-transparent hover:border-blue-200 transition-all">
            <div className="flex items-center space-x-4 mb-6">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Cloud className="h-6 w-6 text-blue-600" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-gray-900">AWS Bedrock</h3>
                <p className="text-gray-600">Powered by Claude 3 Sonnet</p>
              </div>
            </div>
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-700">Advanced reasoning capabilities</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-700">Deep context understanding</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-700">Bedrock Guardrails ready</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-700">Enterprise-grade security</span>
              </div>
            </div>
          </div>

          {/* NVIDIA NIM Card */}
          <div className="bg-white rounded-xl shadow-lg p-8 border-2 border-transparent hover:border-green-200 transition-all">
            <div className="flex items-center space-x-4 mb-6">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <Cpu className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-gray-900">NVIDIA NIM</h3>
                <p className="text-gray-600">Nemotron Nano 8B + Retrieval Embeddings</p>
              </div>
            </div>
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-700">Agentic reasoning model</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-700">RAG-powered context retrieval</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-700">Semantic search embeddings</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm text-gray-700">NeMo compatible</span>
              </div>
            </div>
          </div>
        </div>

        {/* MCP Tool Selection */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-12">
          <h3 className="text-2xl font-semibold text-gray-900 mb-6 text-center">
            Select Tools for Orchestration
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {[
              { id: 'gemini', name: 'Gemini', icon: '🤖' },
              { id: 'figma', name: 'Figma', icon: '🎨' },
              { id: 'openai', name: 'ChatGPT', icon: '💬' },
              { id: 'github', name: 'GitHub', icon: '🐙' },
              { id: 'cursor', name: 'Cursor', icon: '⚡' }
            ].map((tool) => (
              <button
                key={tool.id}
                onClick={() => handleToolToggle(tool.id)}
                className={`p-4 rounded-lg border-2 transition-all ${
                  selectedTools.includes(tool.id)
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="text-2xl mb-2">{tool.icon}</div>
                <div className="text-sm font-medium text-gray-900">{tool.name}</div>
              </button>
            ))}
          </div>
          <div className="mt-4 text-center text-sm text-gray-500">
            Selected: {selectedTools.length} tool{selectedTools.length !== 1 ? 's' : ''}
          </div>
        </div>

        {/* Agentic AI Architecture Card */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-8 text-white mb-12">
          <div className="flex items-center space-x-4 mb-8">
            <div className="w-12 h-12 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
              <Brain className="h-6 w-6" />
            </div>
            <div>
              <h3 className="text-2xl font-semibold">Agentic AI Architecture</h3>
              <p className="text-blue-100">Multi-tool orchestration powered by MCP</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-pink-500 rounded-lg flex items-center justify-center">
                <Brain className="h-5 w-5" />
              </div>
              <div>
                <h4 className="font-semibold">Reasoning Engine</h4>
                <p className="text-sm text-blue-100">Nemotron Nano 8B</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-purple-500 rounded-lg flex items-center justify-center">
                <div className="w-3 h-3 bg-white rounded-full"></div>
              </div>
              <div>
                <h4 className="font-semibold">Retrieval System</h4>
                <p className="text-sm text-blue-100">Embedding NIM</p>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { action: 'Ideate', icon: '💡' },
              { action: 'Plan', icon: '📋' },
              { action: 'Design', icon: '🎨' },
              { action: 'Execute', icon: '🚀' }
            ].map(({ action, icon }) => (
              <button
                key={action}
                onClick={() => handleAction(action)}
                disabled={isOrchestrating}
                className="bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg p-4 flex items-center space-x-3 transition-all disabled:opacity-50"
              >
                <Zap className="h-5 w-5" />
                <span className="font-medium">{action}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Get Started Button */}
        <div className="text-center">
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-8 rounded-lg text-lg transition-colors duration-200">
            Get Started
          </button>
          <p className="mt-4 text-sm text-gray-500">
            Switch between AI providers anytime in Settings
          </p>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-center">
            <div className="text-gray-500">
              <p>Built with ❤️ using React, FastAPI, and MCP Server</p>
            </div>
            <button className="p-2 text-gray-400 hover:text-gray-600">
              <HelpCircle className="h-5 w-5" />
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}