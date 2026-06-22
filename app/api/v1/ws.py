from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websockets import manager

router = APIRouter()

@router.websocket("/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"System update: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)