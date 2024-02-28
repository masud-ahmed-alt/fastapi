import asyncio
from fastapi import  FastAPI, Request,WebSocket
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

import uvicorn
from . import models
from . database import engine
from .routers import post, user,auth
from typing import List


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)




# CORS middleware to allow requests from any origin, including WebSocket connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# List to store API call logs
api_calls = []


# Function to get formatted API call logs
def get_formatted_logs() -> List[str]:
    return [f"{call['start_time']} - {call['end_time']} : {call['method']} {call['path']}" for call in api_calls]


# Route to show API call logs
@app.get("/console")
async def show_console():
    return {"logs": get_formatted_logs()}


# WebSocket route to stream real-time API call logs
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json({"logs": get_formatted_logs()})
        await asyncio.sleep(1)


# Middleware to log API calls and current time
@app.middleware("http")
async def log_api_calls(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    end_time = datetime.now()
    api_calls.append({
        "path": request.url.path,
        "method": request.method,
        "start_time": start_time,
        "end_time": end_time
    })
    return response



if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)