from typing import Dict, Set
from fastapi import WebSocket
import asyncio


class ConnectionManager:
    """In-memory mapping from user_id -> set[WebSocket]."""

    def __init__(self) -> None:
        self.active: Dict[str, Set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, user_id: str, ws: WebSocket) -> None:
        """Establishes a WebSocket connection for a given user."""
        await ws.accept()
        async with self._lock:
            self.active.setdefault(user_id, set()).add(ws)

    async def disconnect(self, user_id: str, ws: WebSocket) -> None:
        """Disconnects a WebSocket connection for a given user."""
        async with self._lock:
            conns = self.active.get(user_id)
        if conns and ws in conns:
            conns.remove(ws)
        if not conns:
            self.active.pop(user_id, None)

    async def send_to_user(self, user_id: str, payload: dict) -> int:
        """Send to all sockets for a given user. Returns number of deliveries."""
        async with self._lock:
            conns = list(self.active.get(user_id, set()))
        delivered = 0

        dead = []
        for ws in conns:
            try:
                await ws.send_json(payload)
                delivered += 1
            except Exception:
                dead.append(ws)
        for ws in dead:
            await self.disconnect(user_id, ws)

        return delivered


manager = ConnectionManager()
