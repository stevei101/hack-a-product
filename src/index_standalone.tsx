import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { 
  Cloud, 
  Cpu, 
  Brain, 
  Zap, 
  Lightbulb, 
  Target, 
  Palette, 
  Play,
  HelpCircle,
  Check,
  X,
  ArrowRight,
  Loader2
} from 'lucide-react';
import "./index.css";

const App = () => {
  const [showModal, setShowModal] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  
  // Mock MCP data for testing
  const mockTools = [
    { id: 'gemini', name: 'Google Gemini', status: 'available' },
    { id: 'openai', name: 'OpenAI ChatGPT', status: 'available' },
    { id: 'figma', name: 'Figma', status: 'unavailable' }
  ];
  
  const mockTemplates = [
    { id: 'ideation_workflow', name: 'AI Ideation Workflow', tools: ['gemini', 'openai'] },
    { id: 'design_workflow', name: 'Design & Code Workflow', tools: ['figma', 'cursor'] }
  ];

  const handleGetStarted = () => {
    setShowModal(true);
  };

  const handleStartWorkflow = async () => {
    if (selectedProvider) {
      setIsExecuting(true);
      
      // Simulate workflow execution
      setTimeout(() => {
        alert(`✅ Mock workflow completed with ${selectedProvider}!\n\nThis is a frontend-only test - no backend required.`);
        setShowModal(false);
        setIsExecuting(false);
      }, 2000);
    }
  };

  const aiProviders = [
    {
      id: 'aws-bedrock',
      name: 'AWS Bedrock',
      description: 'Claude 3 Sonnet with enterprise security',
      icon: <Cloud className="w-6 h-6 text-blue-600" />,
      features: ['Advanced reasoning', 'Deep context', 'Guardrails ready']
    },
    {
      id: 'nvidia-nim',
      name: 'NVIDIA NIM',
      description: 'Nemotron Nano 8B with RAG embeddings',
      icon: <Cpu className="w-6 h-6 text-green-600" />,
      features: ['Agentic reasoning', 'RAG retrieval', 'Semantic search']
    },
    {
      id: 'mcp-orchestration',
      name: 'MCP Orchestration',
      description: 'Multi-tool workflow coordination',
      icon: <Brain className="w-6 h-6 text-purple-600" />,
      features: ['Tool coordination', 'Workflow templates', 'Parallel execution']
    }
  ];

  return (
    <div className="min-h-screen bg-gray-100 font-sans text-gray-900">
      {/* Header */}
      <header className="py-8 text-center">
        <div className="flex items-center justify-center space-x-3 mb-2">
          <div className="relative">
            <div className="h-8 w-8 bg-blue-500 rounded-lg transform rotate-45"></div>
            <Zap className="h-5 w-5 text-white absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
          </div>
          <h1 className="text-3xl font-extrabold text-gray-900">The Product Mindset</h1>
        </div>
        <h2 className="text-5xl font-extrabold text-gray-900 mt-4 leading-tight">AI-Powered Ideation & Design Companion</h2>
        <p className="text-xl text-gray-600 mt-3">Built for the AWS & NVIDIA Hackathon</p>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* AWS Bedrock Card */}
          <div className="p-6 rounded-xl shadow-lg bg-white text-gray-800">
            <div className="text-center mb-4">
              <div className="text-blue-600 mx-auto mb-3">
                <Cloud className="h-8 w-8" />
              </div>
              <h3 className="text-xl font-semibold">AWS Bedrock</h3>
              <p className="text-sm text-gray-600 mt-1">Powered by Claude 3 Sonnet</p>
            </div>
            <ul className="text-left text-sm text-gray-700 space-y-1 mt-4">
              <li className="flex items-center">
                <Check className="h-4 w-4 text-green-500 mr-2" /> Advanced reasoning capabilities
              </li>
              <li className="flex items-center">
                <Check className="h-4 w-4 text-green-500 mr-2" /> Deep context understanding
              </li>
              <li className="flex items-center">
                <Check className="h-4 w-4 text-green-500 mr-2" /> Bedrock Guardrails ready
              </li>
              <li className="flex items-center">
                <Check className="h-4 w-4 text-green-500 mr-2" /> Enterprise-grade security
              </li>
            </ul>
          </div>

          {/* NVIDIA NIM Card */}
          <div className="p-6 rounded-xl shadow-lg bg-white text-gray-800">
            <div className="text-center mb-4">
              <div className="text-green-600 mx-auto mb-3">
                <Cpu className="h-8 w-8" />
              </div>
              <h3 className="text-xl font-semibold">NVIDIA NIM</h3>
              <p className="text-sm text-gray-600 mt-1">Nemotron Nano 8B + Retrieval Embeddings</p>
            </div>
            <ul className="text-left text-sm text-gray-700 space-y-1 mt-4">
              <li className="flex items-center">
                <Check className="h-4 w-4 text-green-500 mr-2" /> Agentic reasoning model
              </li>
              <li className="flex items-center">
                <Check className="h-4 w-4 text-green-500 mr-2" /> RAG-powered context retrieval
              </li>
              <li className="flex items-center">
                <Check className="h-4 w-4 text-green-500 mr-2" /> Semantic search embeddings
              </li>
              <li className="flex items-center">
                <Check className="h-4 w-4 text-green-500 mr-2" /> NeMo compatible
              </li>
            </ul>
          </div>
        </div>

        {/* Agentic AI Architecture Card */}
        <div className="p-8 rounded-xl shadow-lg bg-gradient-to-br from-purple-600 to-indigo-700 text-white">
          <div className="flex items-center space-x-4 mb-6">
            <Brain className="h-10 w-10 text-pink-300" />
            <h3 className="text-3xl font-bold">Agentic AI Architecture</h3>
          </div>
          
          {/* Top Section - Reasoning Engine & Retrieval System */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="bg-white bg-opacity-20 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <Brain className="w-6 h-6 text-pink-300 mr-2" />
                <span className="text-white font-medium">Reasoning Engine</span>
              </div>
              <p className="text-white text-sm">Nemotron Nano 8B</p>
            </div>
            <div className="bg-white bg-opacity-20 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <div className="w-6 h-6 bg-purple-300 rounded-full mr-2"></div>
                <span className="text-white font-medium">Retrieval System</span>
              </div>
              <p className="text-white text-sm">Embedding NIM</p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button className="bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg p-4 flex flex-col items-center transition-all duration-200">
              <Zap className="w-6 h-6 text-white mb-2" />
              <span className="text-white font-medium">Ideate</span>
            </button>
            <button className="bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg p-4 flex flex-col items-center transition-all duration-200">
              <Target className="w-6 h-6 text-white mb-2" />
              <span className="text-white font-medium">Plan</span>
            </button>
            <button className="bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg p-4 flex flex-col items-center transition-all duration-200">
              <Palette className="w-6 h-6 text-white mb-2" />
              <span className="text-white font-medium">Design</span>
            </button>
            <button className="bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg p-4 flex flex-col items-center transition-all duration-200">
              <Play className="w-6 h-6 text-white mb-2" />
              <span className="text-white font-medium">Execute</span>
            </button>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="text-center">
          <button 
            onClick={handleGetStarted}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg text-lg transition-colors duration-200 mb-4"
          >
            Get Started
          </button>
          <p className="text-gray-600 text-sm mb-4">
            Switch between AI providers anytime in Settings
          </p>
          <div className="flex justify-end">
            <button className="w-8 h-8 bg-gray-300 hover:bg-gray-400 rounded-full flex items-center justify-center transition-colors duration-200">
              <HelpCircle className="w-4 h-4 text-gray-600" />
            </button>
          </div>
        </div>
      </main>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold text-gray-900">Choose Your AI Provider</h3>
              <button 
                onClick={() => setShowModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="space-y-4 mb-6">
              {aiProviders.map((provider) => (
                <div 
                  key={provider.id}
                  className={`border-2 rounded-lg p-4 cursor-pointer transition-all ${
                    selectedProvider === provider.id 
                      ? 'border-blue-500 bg-blue-50' 
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => setSelectedProvider(provider.id)}
                >
                  <div className="flex items-center mb-2">
                    {provider.icon}
                    <h4 className="text-lg font-semibold text-gray-900 ml-3">{provider.name}</h4>
                  </div>
                  <p className="text-gray-600 mb-2">{provider.description}</p>
                  <div className="flex flex-wrap gap-2">
                    {provider.features.map((feature, index) => (
                      <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-sm">
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
            
            <div className="space-y-4">
              {/* Mock MCP Server Status */}
              <div className="p-3 bg-green-100 border border-green-400 text-green-700 rounded-lg text-sm">
                <strong>Frontend Test Mode:</strong> {mockTools.length} tools available (mock data)
              </div>
              
              <div className="flex justify-end space-x-3">
                <button 
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800"
                >
                  Cancel
                </button>
                <button 
                  onClick={handleStartWorkflow}
                  disabled={!selectedProvider || isExecuting}
                  className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white px-6 py-2 rounded-lg flex items-center"
                >
                  {isExecuting ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin mr-2" />
                      Executing...
                    </>
                  ) : (
                    <>
                      Start Workflow
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

createRoot(document.getElementById("root")!).render(<App />);
