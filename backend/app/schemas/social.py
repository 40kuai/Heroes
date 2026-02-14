from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FriendRequest(BaseModel):
    user_id: int
    friend_id: int


class FriendResponse(BaseModel):
    id: int
    user_id: int
    friend_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageRequest(BaseModel):
    sender_id: int
    receiver_id: int
    content: str


class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
