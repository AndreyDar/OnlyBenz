from fastapi import FastAPI
from .routers import root, login, chat_client_data_structure, shell_api, chat_client_data

app = FastAPI()

app.include_router(root.router)
app.include_router(login.router)
app.include_router(chat_client_data.router)
app.include_router(chat_client_data_structure.router)
app.include_router(shell_api.router)