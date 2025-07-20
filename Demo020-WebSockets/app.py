from fastapi import Cookie, Depends, FastAPI, Query, responses, status
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from fastapi import websockets
from pathlib import Path
from typing import Annotated

import ws_1.route
import ws_2.route
import ws_3.route


app: FastAPI = FastAPI()
app.include_router(ws_1.route.router)
app.include_router(ws_2.route.router)
app.include_router(ws_3.route.router)
