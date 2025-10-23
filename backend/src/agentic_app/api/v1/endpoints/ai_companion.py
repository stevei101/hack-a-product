from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from agentic_app.services.ai_companion_service import (
    ai_companion_service,
    AICompanionRequest,
    AICompanionResponse,
    AICompanionMessage
)
from agentic_app.models.project import Project, ChatMessage
from agentic_app.core.sync_database import get_sync_db

router = APIRouter()


@router.post("/chat", response_model=AICompanionResponse)
async def chat_with_ai_companion(
    request: AICompanionRequest,
    db: Session = Depends(get_sync_db)
):
    """Chat with the AI Companion - it can use tools to help you!"""
    try:
        # Process the message with AI Companion service
        response = await ai_companion_service.process_message(request)
        
        # Save the conversation to database
        if request.project_id:
            # Save user message
            user_message = ChatMessage(
                project_id=request.project_id,
                message_type='user',
                content=request.message,
                timestamp=datetime.utcnow(),
                ai_provider=request.ai_provider
            )
            db.add(user_message)
            db.flush()  # Get the ID
            
            # Save AI response
            ai_message = ChatMessage(
                project_id=request.project_id,
                message_type='ai',
                content=response.message.content,
                timestamp=response.message.timestamp,
                ai_provider=response.message.ai_provider,
                model_version=response.message.model_version,
                tokens_used=response.message.tokens_used
            )
            db.add(ai_message)
            db.commit()
            
            # Update response message IDs
            response.message.id = ai_message.id
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Companion error: {str(e)}")


@router.get("/tools", response_model=List[dict])
async def get_available_tools():
    """Get list of tools available to the AI Companion."""
    try:
        tools = await ai_companion_service.get_available_tools()
        return tools
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tools: {str(e)}")


@router.post("/suggest-tools")
async def suggest_tools_for_message(message: str):
    """Suggest tools that might be helpful for a given message."""
    try:
        suggested_tools = await ai_companion_service.suggest_tools_for_message(message)
        return {
            "message": message,
            "suggested_tools": suggested_tools,
            "reasoning": f"Based on keywords in your message, these tools might be helpful: {', '.join(suggested_tools)}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error suggesting tools: {str(e)}")


@router.get("/projects/{project_id}/chat-history")
def get_chat_history(project_id: int, db: Session = Depends(get_sync_db)):
    """Get chat history for a specific project."""
    try:
        messages = db.query(ChatMessage).filter(
            ChatMessage.project_id == project_id
        ).order_by(ChatMessage.timestamp.asc()).all()
        
        return {
            "project_id": project_id,
            "messages": [
                {
                    "id": msg.id,
                    "message_type": msg.message_type,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "ai_provider": msg.ai_provider,
                    "model_version": msg.model_version,
                    "tokens_used": msg.tokens_used
                }
                for msg in messages
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat history: {str(e)}")


@router.post("/projects/{project_id}/clear-chat")
def clear_chat_history(project_id: int, db: Session = Depends(get_sync_db)):
    """Clear chat history for a specific project."""
    try:
        # Delete all chat messages for the project
        deleted_count = db.query(ChatMessage).filter(
            ChatMessage.project_id == project_id
        ).delete()
        
        db.commit()
        
        return {
            "project_id": project_id,
            "deleted_messages": deleted_count,
            "message": f"Cleared {deleted_count} messages from chat history"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing chat history: {str(e)}")


@router.get("/projects/{project_id}/chat-summary")
def get_chat_summary(project_id: int, db: Session = Depends(get_sync_db)):
    """Get a summary of the chat conversation for a project."""
    try:
        messages = db.query(ChatMessage).filter(
            ChatMessage.project_id == project_id
        ).order_by(ChatMessage.timestamp.asc()).all()
        
        if not messages:
            return {
                "project_id": project_id,
                "summary": "No conversation history yet",
                "message_count": 0,
                "tools_used": []
            }
        
        # Analyze conversation
        user_messages = [msg for msg in messages if msg.message_type == 'user']
        ai_messages = [msg for msg in messages if msg.message_type == 'ai']
        
        # Extract tools used
        tools_used = set()
        for msg in ai_messages:
            if msg.tokens_used:  # Indicates AI response
                # This would need to be enhanced to track actual tool usage
                pass
        
        return {
            "project_id": project_id,
            "summary": f"Conversation with {len(user_messages)} user messages and {len(ai_messages)} AI responses",
            "message_count": len(messages),
            "tools_used": list(tools_used),
            "last_activity": messages[-1].timestamp.isoformat() if messages else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chat summary: {str(e)}")


@router.post("/test-tool-execution")
async def test_tool_execution(tool_name: str, test_message: str):
    """Test tool execution for debugging purposes."""
    try:
        # Analyze message for tools
        analysis = await ai_companion_service._analyze_message_for_tools(test_message)
        
        # Execute tools if recommended
        executions = []
        if tool_name in analysis['recommended_tools']:
            executions = await ai_companion_service._execute_recommended_tools(
                test_message, 
                [tool_name], 
                None
            )
        
        return {
            "tool_name": tool_name,
            "test_message": test_message,
            "analysis": analysis,
            "executions": executions,
            "success": len(executions) > 0 and executions[0].get('status') == 'success'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing tool execution: {str(e)}")
