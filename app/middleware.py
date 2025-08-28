import os
from typing import Optional
from fastapi import Header, HTTPException

API_TOKEN = os.getenv("API_TOKEN")


def verify_token(token: Optional[str] = Header(default=None)):
    if API_TOKEN and token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")
