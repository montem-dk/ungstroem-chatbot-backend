from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from services.chatbase_service import ChatbaseHandler

router = APIRouter(prefix="/chat", tags=["Chat"])
chatbase_handler = ChatbaseHandler()

@router.post("")
async def chat_endpoint(payload: dict):
    messages = payload.get("messages", "")
    msg_to_send = ""
    for msg in messages:
        if msg.get("sender") == "user":
            msg_to_send = msg_to_send + f"User: {msg.get("text", "")}" + "\n"
        elif msg.get("sender") == "bot":
            msg_to_send = msg_to_send + f"Bot: {msg.get("text", "")}" + "\n"
    generator = chatbase_handler.read_chatbot_reply(msg_to_send)
    return StreamingResponse(generator, media_type="text/plain")
