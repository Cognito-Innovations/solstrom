from pydantic import BaseModel, Field
from datetime import datetime, UTC

class Message(BaseModel):
    user_id: str
    user_message: str
    agent_message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))