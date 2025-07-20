from fastapi import APIRouter, Cookie, Depends, FastAPI, Query, responses
from fastapi import status, WebSocket, WebSocketDisconnect, WebSocketException
from fastapi import websockets
from pathlib import Path
from string import Template
from typing import Annotated

import asyncio
import json


router: APIRouter = APIRouter(prefix='/demo/3')

BASE_DiR = Path(__file__).parent.resolve()

html_file = BASE_DiR / 'index.html'
html_content: str = html_file.read_text()


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[websockets.WebSocket] = []

    async def broadcast(self, message: str):
        await asyncio.gather(
            *(conn.send_text(message) for conn in self.active_connections)
        )

    async def connect(self, websocket: websockets.WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: websockets.WebSocket):
        print(len(self.active_connections))
        self.active_connections.remove(websocket)
        print(len(self.active_connections))

    async def send_personal_message(
        self, websocket: websockets.WebSocket, message: str
    ):
        await websocket.send_text(message)


manager: ConnectionManager = ConnectionManager()


@router.get('')
async def get(client_id: str):
    return responses.HTMLResponse(
        Template(html_content).safe_substitute(client_id=client_id)
    )


@router.websocket('/ws/{client_id}')
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    client_id: str,
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == 'exit 0':
                await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)
                await manager.broadcast(
                    json.dumps({'message': f'{client_id} Exits'})
                )
                break
            else:
                await manager.broadcast(
                    json.dumps({'client_id': client_id, 'message': data})
                )
                # await manager.send_personal_message(
                #     websocket,
                #     orjson.dumps({'client_id': client_id, 'message': data}),
                # )
                # await websocket.send_text(f'Message from client was: {data}')

    except websockets.WebSocketDisconnect as we:
        await manager.disconnect(websocket)
        await manager.broadcast(
            json.dumps(
                {'client_id': client_id, 'message': f'{client_id} left chat'}
            )
        )
