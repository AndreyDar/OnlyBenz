from httpx import AsyncClient

async def get_chat_client_response():
    async with AsyncClient() as client:
        response = await client.get('https://api.chatclient.com/messages')
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch messages", "status_code": response.status_code}
