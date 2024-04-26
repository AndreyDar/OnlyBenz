from fastapi import APIRouter
from ..api.shell_api import call_shell_api_with_curl

router = APIRouter()

@router.get("/curl-shell-api-data/")
def curl_shell_api_data():
    return {"data": call_shell_api_with_curl()}
