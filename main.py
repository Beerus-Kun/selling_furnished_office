# from collections import defaultdict
from typing import Optional, List, Union, Dict
from fastapi import FastAPI,  WebSocketDisconnect, Cookie, Depends, Query, status, WebSocket
from typing import Union
# from starlette.websockets import WebSocket
# from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, status

from fastapi.responses import HTMLResponse
import schemas.account as SCAccount
import uvicorn
import model.connect as Connect
from model import comment as CommentDB
from dotenv import load_dotenv
from routers import account, product, bill, comment, static
load_dotenv()

app = FastAPI()

app.include_router(
    account.router,
    prefix='/account',
    tags=['account']
    )

app.include_router(
    product.router,
    prefix='/product',
    tags=['product']
)

app.include_router(
    bill.router,
    prefix='/bill',
    tags=['bill']
)

app.include_router(
    comment.router,
    prefix='/comment',
    tags=['comment']
)

app.include_router(
    static.router,
    prefix='/static',
    tags=['static']
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: int):
        print(websocket)
        await websocket.accept()
        if self.active_connections.get(room) == None:
            self.active_connections[room] = [websocket]
        else:
            self.active_connections[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room:int):
        self.active_connections[room].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message, room:int):
        for connection in self.active_connections[room]:
            await connection.send_json(message)

manager = ConnectionManager()



@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            res = CommentDB.getComment(client_id)
            await manager.broadcast(res, client_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        print(f"Client #{client_id} left the chat", client_id)
        # await manager.broadcast(f"Client #{client_id} left the chat", client_id)


if __name__ == "__main__":
    uvicorn.run(app)