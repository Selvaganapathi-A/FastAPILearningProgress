from fastapi import APIRouter, Cookie, Depends, Query, responses, status
from fastapi import websockets
from pathlib import Path
from typing import Annotated, Any


router: APIRouter = APIRouter(prefix='/demo/2')

BASE_DiR = Path(__file__).parent.resolve()

html_file = BASE_DiR / 'index.html'
html: str = html_file.read_text()


@router.get('/')
async def get():
    return responses.HTMLResponse(html)


async def get_token_and_session(
    token: Annotated[str, Query()],
    session: Annotated[str | None, Cookie()] = None,
):
    message = {}
    message['session'] = session or '0'
    message['token'] = token
    return message


@router.websocket('/{room_no}/ws')
async def websocket_endpoint(
    *,
    websocket: websockets.WebSocket,
    room_no: Annotated[str, Path()],
    query: str | None = None,
    cookie_and_token: Annotated[dict[str, Any], Depends(get_token_and_session)],
):
    await websocket.accept()
    try:
        if query:
            await websocket.send_text(
                f'Speech from {room_no} related to {query}.'
            )
        await websocket.send_text(f'Session {cookie_and_token["session"]}')
        await websocket.send_text(f'Token : {cookie_and_token["token"]}')
        await websocket.send_text('<hr>')
        while True:
            data = await websocket.receive_text()
            if data == 'exit 0':
                await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)
                break
            else:
                await websocket.send_text(
                    f'Message from client in {room_no} : {data}'
                )
                print(data)
    except websockets.WebSocketDisconnect as we:
        print('Connection Closed')
