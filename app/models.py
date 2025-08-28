from pydantic import BaseModel, Field
from typing import Any, Optional


# TODO: think about fields
class NotificationRequest(BaseModel):
    user_id: str = Field(..., description="Recipient user identifier")
    type: str = Field("info", description="Notification type")
    message: str = Field(..., description="Human-readable message")
    data: Optional[Any] = Field(None, description="Arbitrary JSON payload")
