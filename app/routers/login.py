from fastapi import APIRouter, Cookie
from starlette.responses import JSONResponse

router = APIRouter()

@router.post("/login/")
async def login():
    response = JSONResponse(content={"message": "You are logged in"})
    response.set_cookie(key="session_id", value="fake-session-id")
    return response