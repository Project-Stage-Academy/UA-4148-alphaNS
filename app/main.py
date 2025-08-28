from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from models import NotificationRequest
from manager import manager
from middleware import verify_token

load_dotenv()

app = FastAPI(title="Notification Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.post("/notify", dependencies=[Depends(verify_token)])
async def notify(req: NotificationRequest):
    # Add persistence (store notifications somewhere)
    # for later retrieval when user comes back online.
    payload = {
        "user_id": req.user_id,
        "type": req.type,
        "message": req.message,
        "data": req.data,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    delivered = await manager.send_to_user(req.user_id, payload)
    return {"delivered": delivered, "payload": payload}


# TODO: replace user_id with JWT token
@app.websocket("/ws/{user_id}")
async def ws_user(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            # Messages from clients ignored
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(user_id, websocket)
