from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.schemas.agent import (
    AgentRequest,
    AgentResponse
)

from backend.services.agent_service import AgentService

agent_service = AgentService()

router = APIRouter()


@router.get("/health")
async def health():

    return {
        "status": "healthy"
    }


@router.post(
    "/ask",
    response_model=AgentResponse
)
async def ask_agent(
    request: AgentRequest
):

    answer = agent_service.ask(
        request.question,
        request.session_id
    )

    return AgentResponse(
        answer=answer
    )
@router.post("/ask/stream")
async def stream_agent(
    request: AgentRequest
):

    return StreamingResponse(
        agent_service.stream(
            request.question,
            request.session_id
        ),
        media_type="text/plain"
    )   
