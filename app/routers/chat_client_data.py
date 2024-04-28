from fastapi import APIRouter
from ..api.chatgpt import chat_with_gpt

router = APIRouter()

@router.get("/chat-client-messages/")
async def chat(prompt):
    return {"response": chat_with_gpt(prompt)}