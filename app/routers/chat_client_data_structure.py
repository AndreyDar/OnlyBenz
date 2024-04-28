from fastapi import APIRouter
from app.api.gpt_datastructured_test import generate_description

router = APIRouter()


@router.post("/chat-structure/")
async def chat_client_messages(raw_message):
    car_recommendation = generate_description(raw_message)
    return await {"car_recommendation": car_recommendation}
