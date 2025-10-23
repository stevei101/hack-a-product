from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .service import OrchestrationService

router = APIRouter()
orchestration_service = OrchestrationService()

class OrchestrationRequest(BaseModel):
    tool: str
    prompt: str

@router.post("/orchestrate")
async def orchestrate(request: OrchestrationRequest):
    """
    Receives a request and uses the OrchestrationService to process it.
    """
    try:
        result = await orchestration_service.process_request(request.tool, request.prompt)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
