from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from uuid import uuid4
import asyncio

from shipyard.models import Task

app = FastAPI()


@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    pass


@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    pass


async def run_task(task):
    pass


@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id):
    print(f"Tickitin' {task_id}")


@app.delete("/tasks/{task_id}")
async def delete_task(task_id):
    pass
