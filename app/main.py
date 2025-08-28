from fastapi import Depends, FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from models import NotificationRequest
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
def notify(req: NotificationRequest):
    payload = {
        "user_id": req.user_id,
        "type": req.type,
        "message": req.message,
        "data": req.data,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    return {"delivered": False, "payload": payload}
