from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from multiprocessing import current_process

from fastapi.responses import JSONResponse
from shipyard.envoy.tasks import CloseTunnelTask, OpenTunnelTask
from shipyard.models import SshTunnel, SshTunnelIn
from shipyard.tasks import ProcessIdPrintingTask, TaskRunner, ThreadInfoTask, LongSleeperTask
import asyncio

app = FastAPI()

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Server error: {exc}"},
    )

@app.get("/")
async def root():
    result = await TaskRunner.run_task_async(LongSleeperTask())
    return {"message": f"Hello Breh {result}"}

@app.get("/pid")
async def pid_task():
    with TaskRunner.async_task_client() as conn:
        await conn.coro_send(ProcessIdPrintingTask())
        return await conn.coro_recv()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        pass

@app.websocket("/ws2")
async def websocket_reporter(websocket: WebSocket):
    await websocket.accept()
    for i in range(1,10):
        await websocket.send_text(f"Message text was: {i}")
        await asyncio.sleep(1)
    await websocket.close()

@app.get("/tunnel")
def list_tunnels():
    return TaskRunner.run_task_sync(ThreadInfoTask())

@app.post("/tunnel")
def create_tunnel(ssh_in: SshTunnelIn):
    ssh = SshTunnel.from_input(ssh_in)
    return TaskRunner.run_task(OpenTunnelTask(ssh=ssh))

@app.delete("/tunnel")
def close_tunnel(ssh_in: SshTunnelIn):
    ssh = SshTunnel.from_input(ssh_in)
    return TaskRunner.run_task(CloseTunnelTask(ssh=ssh))

@app.post("/tunnel/{ship_name}")
def create_tunnel_ship(ship_name: str):
    ssh = SshTunnel(url=f"ssh://john@bitcoin.rondev.live:4344", local_port=8888, remote_port=9002) # pyright:ignore
    return TaskRunner.run_task(OpenTunnelTask(ssh=ssh))

@app.delete("/tunnel/{ship_name}")
def close_tunnel_ship(ship_name: str):
    ssh = SshTunnel(url=f"ssh://john@bitcoin.rondev.live:4344", local_port=8888, remote_port=9002) # pyright:ignore
    return TaskRunner.run_task(CloseTunnelTask(ssh=ssh))
