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
  ArrowRight
} from 'lucide-react';
import "./index.css";

const App = () => {
  const [showModal, setShowModal] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState('');

  const handleGetStarted = () => {
    setShowModal(true);
  };

  const handleStartWorkflow = () => {
    if (selectedProvider) {
      // Here we would typically call the MCP server API
      console.log(`Starting workflow with ${selectedProvider}`);
      alert(`Starting AI workflow with ${selectedProvider}! This would connect to the MCP server.`);
      setShowModal(false);
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
      features: ['Gemini', 'Figma', 'ChatGPT', 'GitHub', 'Cursor']
    }
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="text-center pt-8 pb-4">
        <div className="flex items-center justify-center mb-4">
          <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center mr-3">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-gray-800">The Product Mindset</h1>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          AI-Powered Ideation & Design Companion
        </h2>
        <p className="text-lg text-gray-600">
          Built for the AWS & NVIDIA Hackathon
        </p>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Top Row - AWS Bedrock & NVIDIA NIM */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* AWS Bedrock Card */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center mb-4">
              <Cloud className="w-8 h-8 text-blue-600 mr-3" />
              <h3 className="text-xl font-semibold text-gray-800">AWS Bedrock</h3>
            </div>
            <p className="text-gray-600 mb-4">Powered by Claude 3 Sonnet.</p>
            <ul className="space-y-2">
              <li className="flex items-center text-gray-700">
                <Check className="w-4 h-4 text-green-500 mr-2" />
                Advanced reasoning capabilities
              </li>
              <li className="flex items-center text-gray-700">
                <Check className="w-4 h-4 text-green-500 mr-2" />
                Deep context understanding
              </li>
              <li className="flex items-center text-gray-700">
                <Check className="w-4 h-4 text-green-500 mr-2" />
                Bedrock Guardrails ready
              </li>
              <li className="flex items-center text-gray-700">
                <Check className="w-4 h-4 text-green-500 mr-2" />
                Enterprise-grade security
              </li>
            </ul>
          </div>

          {/* NVIDIA NIM Card */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center mb-4">
              <Cpu className="w-8 h-8 text-green-600 mr-3" />
              <h3 className="text-xl font-semibold text-gray-800">NVIDIA NIM</h3>
            </div>
            <p className="text-gray-600 mb-4">Nemotron Nano 8B + Retrieval Embeddings.</p>
            <ul className="space-y-2">
              <li className="flex items-center text-gray-700">
                <Check className="w-4 h-4 text-green-500 mr-2" />
                Agentic reasoning model
              </li>
              <li className="flex items-center text-gray-700">
                <Check className="w-4 h-4 text-green-500 mr-2" />
                RAG-powered context retrieval
              </li>
              <li className="flex items-center text-gray-700">
                <Check className="w-4 h-4 text-green-500 mr-2" />
                Semantic search embeddings
              </li>
              <li className="flex items-center text-gray-700">
                <Check className="w-4 h-4 text-green-500 mr-2" />
                NeMo compatible
              </li>
            </ul>
          </div>
        </div>

        {/* Agentic AI Architecture Card */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center mb-6">
            <Brain className="w-8 h-8 text-white mr-3" />
            <h3 className="text-xl font-semibold text-white">Agentic AI Architecture</h3>
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
      </div>

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
            
            <div className="flex justify-end space-x-3">
              <button 
                onClick={() => setShowModal(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Cancel
              </button>
              <button 
                onClick={handleStartWorkflow}
                disabled={!selectedProvider}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white px-6 py-2 rounded-lg flex items-center"
              >
                Start Workflow
                <ArrowRight className="w-4 h-4 ml-2" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

createRoot(document.getElementById("root")!).render(<App />);