from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

# Import Base from sync_database
from agentic_app.core.sync_database import Base


class Project(Base):
    """Project model for storing user projects."""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Project settings and configuration
    ai_provider = Column(String(100), default="nvidia-nim")
    settings = Column(JSON, default=dict)
    
    # Relationships
    chat_messages = relationship("ChatMessage", back_populates="project", cascade="all, delete-orphan")
    workflows = relationship("Workflow", back_populates="project", cascade="all, delete-orphan")
    ideas = relationship("Idea", back_populates="project", cascade="all, delete-orphan")


class ChatMessage(Base):
    """Chat message model for AI Companion conversations."""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    message_type = Column(String(20), nullable=False)  # 'user' or 'ai'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # AI-specific fields
    ai_provider = Column(String(100), nullable=True)
    model_version = Column(String(50), nullable=True)
    tokens_used = Column(Integer, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="chat_messages")


class Workflow(Base):
    """Workflow model for storing AI workflows and executions."""
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    workflow_type = Column(String(100), nullable=False)  # 'ideation', 'planning', 'design', 'execution'
    status = Column(String(50), default="pending")  # 'pending', 'running', 'completed', 'failed'
    
    # Workflow configuration
    ai_provider = Column(String(100), nullable=False)
    tools_used = Column(JSON, default=list)
    parameters = Column(JSON, default=dict)
    
    # Execution results
    result = Column(Text, nullable=True)
    execution_time = Column(Integer, nullable=True)  # in seconds
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="workflows")


class Idea(Base):
    """Idea model for storing project ideas and concepts."""
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)  # 'feature', 'improvement', 'bug', 'research'
    priority = Column(String(20), default="medium")  # 'low', 'medium', 'high', 'critical'
    status = Column(String(50), default="new")  # 'new', 'in_progress', 'completed', 'rejected'
    
    # AI-generated content
    ai_generated = Column(Boolean, default=False)
    ai_provider = Column(String(100), nullable=True)
    confidence_score = Column(Integer, nullable=True)  # 0-100
    
    # Metadata
    tags = Column(JSON, default=list)
    attachments = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="ideas")


class UserSettings(Base):
    """User settings and tool configuration model."""
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=False, index=True)  # Could be email or UUID
    
    # AI Provider configurations
    default_ai_provider = Column(String(100), default="nvidia-nim")
    ai_provider_configs = Column(JSON, default=dict)
    
    # MCP Tool configurations
    mcp_tool_configs = Column(JSON, default=dict)
    
    # General settings
    dark_mode = Column(Boolean, default=False)
    auto_save = Column(Boolean, default=True)
    notifications = Column(Boolean, default=True)
    
    # Other preferences
    preferences = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)