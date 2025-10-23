from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session

from agentic_app.models.project import Project, UserSettings, ChatMessage, Workflow
from agentic_app.core.sync_database import get_sync_db

router = APIRouter()


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    ai_provider: str = "nvidia-nim"
    settings: Optional[dict] = {}


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    ai_provider: Optional[str] = None
    settings: Optional[dict] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str
    ai_provider: str
    settings: dict
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_sync_db)):
    """Create a new project."""
    try:
        db_project = Project(
            name=project.name,
            description=project.description,
            ai_provider=project.ai_provider,
            settings=project.settings or {}
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        return ProjectResponse.from_orm(db_project)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating project: {str(e)}")


@router.get("/", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_sync_db)):
    """Get all projects."""
    try:
        projects = db.query(Project).filter(Project.status == "active").all()
        return [ProjectResponse.from_orm(project) for project in projects]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching projects: {str(e)}")


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_sync_db)):
    """Get a specific project by ID."""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return ProjectResponse.from_orm(project)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching project: {str(e)}")


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int, 
    project_update: ProjectUpdate, 
    db: Session = Depends(get_sync_db)
):
    """Update a project."""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Update fields
        if project_update.name is not None:
            project.name = project_update.name
        if project_update.description is not None:
            project.description = project_update.description
        if project_update.status is not None:
            project.status = project_update.status
        if project_update.ai_provider is not None:
            project.ai_provider = project_update.ai_provider
        if project_update.settings is not None:
            project.settings = project_update.settings
        
        project.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(project)
        
        return ProjectResponse.from_orm(project)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating project: {str(e)}")


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_sync_db)):
    """Delete a project (soft delete by setting status to 'deleted')."""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project.status = "deleted"
        project.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {"message": f"Project '{project.name}' deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting project: {str(e)}")


@router.get("/{project_id}/stats")
def get_project_stats(project_id: int, db: Session = Depends(get_sync_db)):
    """Get project statistics."""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Count related records
        chat_count = db.query(ChatMessage).filter(ChatMessage.project_id == project_id).count()
        workflow_count = db.query(Workflow).filter(Workflow.project_id == project_id).count()
        
        return {
            "project_id": project_id,
            "project_name": project.name,
            "chat_messages": chat_count,
            "workflows": workflow_count,
            "created_at": project.created_at.isoformat(),
            "last_updated": project.updated_at.isoformat(),
            "ai_provider": project.ai_provider
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching project stats: {str(e)}")


# User Settings endpoints
class UserSettingsUpdate(BaseModel):
    default_ai_provider: Optional[str] = None
    ai_provider_configs: Optional[dict] = None
    mcp_tool_configs: Optional[dict] = None
    dark_mode: Optional[bool] = None
    auto_save: Optional[bool] = None
    notifications: Optional[bool] = None
    preferences: Optional[dict] = None


@router.get("/settings/{user_id}")
def get_user_settings(user_id: str, db: Session = Depends(get_sync_db)):
    """Get user settings."""
    try:
        settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
        if not settings:
            # Create default settings
            settings = UserSettings(user_id=user_id)
            db.add(settings)
            db.commit()
            db.refresh(settings)
        
        return {
            "user_id": settings.user_id,
            "default_ai_provider": settings.default_ai_provider,
            "ai_provider_configs": settings.ai_provider_configs,
            "mcp_tool_configs": settings.mcp_tool_configs,
            "dark_mode": settings.dark_mode,
            "auto_save": settings.auto_save,
            "notifications": settings.notifications,
            "preferences": settings.preferences,
            "created_at": settings.created_at.isoformat(),
            "updated_at": settings.updated_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user settings: {str(e)}")


@router.put("/settings/{user_id}")
def update_user_settings(
    user_id: str, 
    settings_update: UserSettingsUpdate, 
    db: Session = Depends(get_sync_db)
):
    """Update user settings."""
    try:
        settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
        if not settings:
            settings = UserSettings(user_id=user_id)
            db.add(settings)
        
        # Update fields
        if settings_update.default_ai_provider is not None:
            settings.default_ai_provider = settings_update.default_ai_provider
        if settings_update.ai_provider_configs is not None:
            settings.ai_provider_configs = settings_update.ai_provider_configs
        if settings_update.mcp_tool_configs is not None:
            settings.mcp_tool_configs = settings_update.mcp_tool_configs
        if settings_update.dark_mode is not None:
            settings.dark_mode = settings_update.dark_mode
        if settings_update.auto_save is not None:
            settings.auto_save = settings_update.auto_save
        if settings_update.notifications is not None:
            settings.notifications = settings_update.notifications
        if settings_update.preferences is not None:
            settings.preferences = settings_update.preferences
        
        settings.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(settings)
        
        return {
            "user_id": settings.user_id,
            "message": "Settings updated successfully",
            "updated_at": settings.updated_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user settings: {str(e)}")