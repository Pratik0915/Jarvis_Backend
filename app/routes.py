from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from .models import ChatRequest
from .groq_service import ask_jarvis, ask_jarvis_stream

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):

    response = ask_jarvis(request.messages)

    return {
        "response": response
    }


@router.post("/chat-stream")
async def chat_stream(request: ChatRequest):

    return StreamingResponse(
        ask_jarvis_stream(request.messages),
        media_type="text/plain",
    )