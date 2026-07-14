from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from .models import ChatRequest, ChatResponse
from .ai import ask_jarvis, ask_jarvis_stream

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    reply = ask_jarvis(request.messages)

    return ChatResponse(
        response=reply
    )


@router.post("/chat/stream")
def chat_stream(request: ChatRequest):

    return StreamingResponse(
        ask_jarvis_stream(request.messages),
        media_type="text/plain",
    )