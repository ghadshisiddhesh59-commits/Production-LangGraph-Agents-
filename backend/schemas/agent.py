from pydantic import BaseModel, Field


class AgentRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="User question"
    )

    session_id: str = Field(
        ...,
        min_length=1,
        description="Conversation session ID"
    )


class AgentResponse(BaseModel):

    answer: str