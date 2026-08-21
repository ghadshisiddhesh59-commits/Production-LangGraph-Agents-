import uuid

from fastapi import FastAPI, Request

from backend.api.routes import router
from backend.database.connection import Base, engine
from backend.database.models import ConversationMessage
from backend.logger import logger
from fastapi import HTTPException
from fastapi.responses import JSONResponse

Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Production LangGraph AI Agent",
    version="1.0.0",
    description="Production-level LangGraph AI Agent API"
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.middleware("http")
async def request_id_middleware(
    request: Request,
    call_next
):

    request_id = str(
        uuid.uuid4()
    )

    logger.info(
        "Request started | id=%s | method=%s | path=%s",
        request_id,
        request.method,
        request.url.path
    )

    try:

        response = await call_next(
            request
        )

        response.headers[
            "X-Request-ID"
        ] = request_id

        logger.info(
            "Request completed | id=%s | status=%s",
            request_id,
            response.status_code
        )

        return response

    except Exception:

        logger.exception(
            "Request failed | id=%s",
            request_id
        )

        raise
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    request_id = getattr(
        request.state,
        "request_id",
        "unknown"
    )

    logger.exception(
        "Unhandled application error | id=%s",
        request_id
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "request_id": request_id
        }
    )
app.include_router(router)