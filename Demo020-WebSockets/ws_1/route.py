from fastapi import APIRouter, Cookie, Depends, FastAPI, Query, responses
from fastapi import status, WebSocket, WebSocketDisconnect, WebSocketException
from fastapi import websockets
from pathlib import Path
from typing import Annotated


router: APIRouter = APIRouter(prefix='/demo/1')

BASE_DiR = Path(__file__).parent.resolve()

html_file = BASE_DiR / 'index.html'
html: str = html_file.read_text()


@router.get('/')
async def get():
    return responses.HTMLResponse(html)


@router.websocket('/ws')
async def websocket_endpoint(
    *,
    websocket: WebSocket,
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data == 'exit 0':
                await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)
                break
            else:
                await websocket.send_text(f'Message from client was: {data}')
                print(data)
    except websockets.WebSocketDisconnect as we:
        print('Connection Closed')
