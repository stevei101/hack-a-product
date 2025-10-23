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
  Loader2,
  Plus,
  Folder,
  Settings,
  Bot,
  Send,
  Sparkles
} from 'lucide-react';
import "./index.css";

const App = () => {
  const [showModal, setShowModal] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [showNewProjectModal, setShowNewProjectModal] = useState(false);
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDescription, setNewProjectDescription] = useState('');
  const [chatMessages, setChatMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: "👋 Hello! I'm your Product Mindset AI companion powered by NVIDIA Nemotron Nano with RAG capabilities. I can semantically search your ideas and provide context-aware suggestions. What would you like to work on today?",
      timestamp: "7:30:02 PM"
    }
  ]);
  const [chatInput, setChatInput] = useState('');

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

  const handleNewProject = () => {
    setShowNewProjectModal(true);
  };

  const handleCreateProject = () => {
    if (newProjectName.trim()) {
      const newProject = {
        id: Date.now(),
        name: newProjectName,
        description: newProjectDescription,
        createdAt: new Date().toISOString(),
        status: 'active'
      };
      setProjects([...projects, newProject]);
      setSelectedProject(newProject);
      setNewProjectName('');
      setNewProjectDescription('');
      setShowNewProjectModal(false);
    }
  };

  const handleSelectProject = (project) => {
    setSelectedProject(project);
  };

  const handleSettings = () => {
    setShowSettingsModal(true);
  };

  const handleSendMessage = () => {
    if (chatInput.trim()) {
      const newMessage = {
        id: chatMessages.length + 1,
        type: 'user',
        content: chatInput,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
      };
      setChatMessages([...chatMessages, newMessage]);
      setChatInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
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
    <div className="min-h-screen bg-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-white bg-opacity-20 rounded flex items-center justify-center mr-3">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold">The Product Mindset</h1>
              <p className="text-sm text-purple-100">Your AI-powered ideation & design companion</p>
            </div>
          </div>
          <button 
            onClick={handleSettings}
            className="p-2 hover:bg-white hover:bg-opacity-20 rounded-lg transition-colors"
          >
            <Settings className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Main Layout */}
      <div className="flex h-[calc(100vh-80px)]">
        {/* Left Sidebar - Projects */}
        <div className="w-80 bg-gray-50 border-r border-gray-200 p-6">
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Projects</h2>
            <button 
              onClick={handleNewProject}
              className="w-full bg-black text-white py-3 px-4 rounded-lg flex items-center justify-center hover:bg-gray-800 transition-colors"
            >
              <Plus className="w-4 h-4 mr-2" />
              New Project
            </button>
          </div>
          
          {/* Projects List */}
          {projects.length > 0 ? (
            <div className="space-y-2">
              {projects.map((project) => (
                <div
                  key={project.id}
                  onClick={() => handleSelectProject(project)}
                  className={`p-3 rounded-lg cursor-pointer transition-colors ${
                    selectedProject?.id === project.id
                      ? 'bg-blue-100 border-2 border-blue-300'
                      : 'bg-white border border-gray-200 hover:bg-gray-100'
                  }`}
                >
                  <h3 className="font-medium text-gray-800">{project.name}</h3>
                  {project.description && (
                    <p className="text-sm text-gray-600 mt-1">{project.description}</p>
                  )}
                  <p className="text-xs text-gray-400 mt-1">
                    Created {new Date(project.createdAt).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-64 text-gray-500">
              <Folder className="w-16 h-16 mb-4 opacity-50" />
              <p className="text-center">No projects yet</p>
            </div>
          )}
        </div>

        {/* Center Content */}
        <div className="flex-1 p-6 overflow-y-auto">
          <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                AI-Powered Ideation & Design Companion
              </h2>
              <p className="text-lg text-gray-600">
                Built for the AWS & NVIDIA Hackathon
              </p>
            </div>

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
            </div>
          </div>
        </div>

        {/* Right Sidebar - AI Companion */}
        <div className="w-96 bg-gray-50 border-l border-gray-200 p-6 flex flex-col">
          <div className="mb-6">
            <div className="flex items-center mb-2">
              <div className="w-6 h-6 bg-gradient-to-r from-purple-500 to-blue-500 rounded flex items-center justify-center mr-2">
                <Sparkles className="w-4 h-4 text-white" />
              </div>
              <h2 className="text-lg font-semibold text-gray-800">AI Companion</h2>
            </div>
            <p className="text-sm text-gray-600 mb-3">Your creative thinking partner.</p>
            <div className="inline-flex items-center px-2 py-1 bg-green-100 text-green-700 rounded text-xs font-medium">
              <Zap className="w-3 h-3 mr-1" />
              Nemotron Nano
            </div>
          </div>

          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto mb-4 space-y-4">
            {chatMessages.map((message) => (
              <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] ${message.type === 'user' ? 'order-2' : 'order-1'}`}>
                  {message.type === 'ai' && (
                    <div className="flex items-center mb-1">
                      <div className="w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center mr-2">
                        <Bot className="w-4 h-4 text-white" />
                      </div>
                      <span className="text-xs text-gray-500">AI Companion</span>
                    </div>
                  )}
                  <div className={`p-3 rounded-lg ${
                    message.type === 'user' 
                      ? 'bg-blue-500 text-white' 
                      : 'bg-white border border-gray-200'
                  }`}>
                    <p className="text-sm">{message.content}</p>
                  </div>
                  <p className="text-xs text-gray-400 mt-1">{message.timestamp}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Chat Input */}
          <div className="flex items-end space-x-2">
            <div className="flex-1">
              <textarea
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask anything... (Shift+Enter for new line)"
                className="w-full p-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={2}
              />
            </div>
            <button
              onClick={handleSendMessage}
              className="p-3 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>

          {/* Help Button */}
          <div className="mt-4 flex justify-end">
            <button className="w-8 h-8 bg-gray-600 hover:bg-gray-700 text-white rounded-full flex items-center justify-center transition-colors">
              <HelpCircle className="w-4 h-4" />
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

      {/* New Project Modal */}
      {showNewProjectModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold text-gray-900">Create New Project</h3>
              <button
                onClick={() => setShowNewProjectModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Project Name
                </label>
                <input
                  type="text"
                  value={newProjectName}
                  onChange={(e) => setNewProjectName(e.target.value)}
                  placeholder="Enter project name..."
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description (Optional)
                </label>
                <textarea
                  value={newProjectDescription}
                  onChange={(e) => setNewProjectDescription(e.target.value)}
                  placeholder="Describe your project..."
                  rows={3}
                  className="w-full p-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button
                  onClick={() => setShowNewProjectModal(false)}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreateProject}
                  disabled={!newProjectName.trim()}
                  className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white px-6 py-2 rounded-lg"
                >
                  Create Project
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Settings Modal */}
      {showSettingsModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold text-gray-900">Settings & Tool Configuration</h3>
              <button
                onClick={() => setShowSettingsModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="space-y-6">
              {/* AI Provider Settings */}
              <div>
                <h4 className="text-lg font-semibold text-gray-800 mb-4">AI Provider Configuration</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {aiProviders.map((provider) => (
                    <div key={provider.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center mb-2">
                        {provider.icon}
                        <h5 className="text-md font-medium text-gray-900 ml-2">{provider.name}</h5>
                      </div>
                      <p className="text-sm text-gray-600 mb-3">{provider.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-500">Status: Available</span>
                        <button className="px-3 py-1 bg-green-100 text-green-700 rounded text-xs">
                          Configure
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* MCP Tools Status */}
              <div>
                <h4 className="text-lg font-semibold text-gray-800 mb-4">MCP Tools Status</h4>
                <div className="space-y-2">
                  {mockTools.map((tool) => (
                    <div key={tool.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center">
                        <div className={`w-3 h-3 rounded-full mr-3 ${
                          tool.status === 'available' ? 'bg-green-500' : 'bg-red-500'
                        }`}></div>
                        <span className="font-medium text-gray-800">{tool.name}</span>
                      </div>
                      <span className={`text-xs px-2 py-1 rounded ${
                        tool.status === 'available' 
                          ? 'bg-green-100 text-green-700' 
                          : 'bg-red-100 text-red-700'
                      }`}>
                        {tool.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* General Settings */}
              <div>
                <h4 className="text-lg font-semibold text-gray-800 mb-4">General Settings</h4>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-700">Dark Mode</span>
                    <button className="w-12 h-6 bg-gray-300 rounded-full relative">
                      <div className="w-5 h-5 bg-white rounded-full absolute top-0.5 left-0.5"></div>
                    </button>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-700">Auto-save Projects</span>
                    <button className="w-12 h-6 bg-blue-500 rounded-full relative">
                      <div className="w-5 h-5 bg-white rounded-full absolute top-0.5 right-0.5"></div>
                    </button>
                  </div>
                </div>
              </div>

              <div className="flex justify-end pt-4">
                <button
                  onClick={() => setShowSettingsModal(false)}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
                >
                  Save Settings
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