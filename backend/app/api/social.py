from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.social import Friend, ChatMessage
from app.models.user import User
from app.schemas.social import FriendRequest, FriendResponse, MessageRequest, MessageResponse
from typing import List

router = APIRouter()


@router.post("/friends/send", response_model=FriendResponse)
def send_friend_request(friend_data: FriendRequest, db: Session = Depends(get_db)):
    """发送好友请求"""
    # 检查目标用户是否存在
    target_user = db.query(User).filter(User.id == friend_data.friend_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 检查是否已经发送过好友请求
    existing_request = db.query(Friend).filter(
        Friend.user_id == friend_data.user_id,
        Friend.friend_id == friend_data.friend_id
    ).first()
    if existing_request:
        raise HTTPException(status_code=400, detail="已经发送过好友请求")
    
    # 创建好友请求
    friend_request = Friend(
        user_id=friend_data.user_id,
        friend_id=friend_data.friend_id,
        status="pending"
    )
    db.add(friend_request)
    db.commit()
    db.refresh(friend_request)
    
    return {
        "id": friend_request.id,
        "user_id": friend_request.user_id,
        "friend_id": friend_request.friend_id,
        "status": friend_request.status,
        "created_at": friend_request.created_at
    }


@router.post("/friends/accept", response_model=FriendResponse)
def accept_friend_request(friend_data: FriendRequest, db: Session = Depends(get_db)):
    """接受好友请求"""
    # 查找好友请求
    friend_request = db.query(Friend).filter(
        Friend.user_id == friend_data.friend_id,
        Friend.friend_id == friend_data.user_id,
        Friend.status == "pending"
    ).first()
    if not friend_request:
        raise HTTPException(status_code=404, detail="好友请求不存在")
    
    # 更新好友状态为已接受
    friend_request.status = "accepted"
    db.commit()
    db.refresh(friend_request)
    
    return {
        "id": friend_request.id,
        "user_id": friend_request.user_id,
        "friend_id": friend_request.friend_id,
        "status": friend_request.status,
        "created_at": friend_request.created_at
    }


@router.post("/friends/block", response_model=FriendResponse)
def block_friend(friend_data: FriendRequest, db: Session = Depends(get_db)):
    """拉黑好友"""
    # 查找好友关系
    friend_relation = db.query(Friend).filter(
        ((Friend.user_id == friend_data.user_id) & (Friend.friend_id == friend_data.friend_id)) |
        ((Friend.user_id == friend_data.friend_id) & (Friend.friend_id == friend_data.user_id))
    ).first()
    if not friend_relation:
        raise HTTPException(status_code=404, detail="好友关系不存在")
    
    # 更新好友状态为已拉黑
    friend_relation.status = "blocked"
    db.commit()
    db.refresh(friend_relation)
    
    return {
        "id": friend_relation.id,
        "user_id": friend_relation.user_id,
        "friend_id": friend_relation.friend_id,
        "status": friend_relation.status,
        "created_at": friend_relation.created_at
    }


@router.get("/friends/{user_id}", response_model=List[FriendResponse])
def get_friends(user_id: int, db: Session = Depends(get_db)):
    """获取好友列表"""
    # 查找用户的所有好友关系
    friends = db.query(Friend).filter(
        ((Friend.user_id == user_id) | (Friend.friend_id == user_id)),
        Friend.status == "accepted"
    ).all()
    
    return [{
        "id": friend.id,
        "user_id": friend.user_id,
        "friend_id": friend.friend_id,
        "status": friend.status,
        "created_at": friend.created_at
    } for friend in friends]


@router.post("/messages/send", response_model=MessageResponse)
def send_message(message_data: MessageRequest, db: Session = Depends(get_db)):
    """发送消息"""
    # 检查接收者是否存在
    receiver = db.query(User).filter(User.id == message_data.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="接收者不存在")
    
    # 检查是否是好友关系
    is_friend = db.query(Friend).filter(
        ((Friend.user_id == message_data.sender_id) & (Friend.friend_id == message_data.receiver_id)) |
        ((Friend.user_id == message_data.receiver_id) & (Friend.friend_id == message_data.sender_id)),
        Friend.status == "accepted"
    ).first()
    if not is_friend:
        raise HTTPException(status_code=400, detail="只能给好友发送消息")
    
    # 创建消息
    message = ChatMessage(
        sender_id=message_data.sender_id,
        receiver_id=message_data.receiver_id,
        content=message_data.content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return {
        "id": message.id,
        "sender_id": message.sender_id,
        "receiver_id": message.receiver_id,
        "content": message.content,
        "is_read": message.is_read,
        "created_at": message.created_at
    }


@router.get("/messages/{user_id}/{friend_id}", response_model=List[MessageResponse])
def get_messages(user_id: int, friend_id: int, db: Session = Depends(get_db)):
    """获取与好友的聊天记录"""
    # 检查是否是好友关系
    is_friend = db.query(Friend).filter(
        ((Friend.user_id == user_id) & (Friend.friend_id == friend_id)) |
        ((Friend.user_id == friend_id) & (Friend.friend_id == user_id)),
        Friend.status == "accepted"
    ).first()
    if not is_friend:
        raise HTTPException(status_code=400, detail="只能查看好友的聊天记录")
    
    # 获取聊天记录
    messages = db.query(ChatMessage).filter(
        ((ChatMessage.sender_id == user_id) & (ChatMessage.receiver_id == friend_id)) |
        ((ChatMessage.sender_id == friend_id) & (ChatMessage.receiver_id == user_id))
    ).order_by(ChatMessage.created_at).all()
    
    # 标记收到的消息为已读
    for message in messages:
        if message.receiver_id == user_id and not message.is_read:
            message.is_read = True
    db.commit()
    
    return [{
        "id": message.id,
        "sender_id": message.sender_id,
        "receiver_id": message.receiver_id,
        "content": message.content,
        "is_read": message.is_read,
        "created_at": message.created_at
    } for message in messages]


@router.put("/messages/read/{message_id}", response_model=MessageResponse)
def mark_message_as_read(message_id: int, db: Session = Depends(get_db)):
    """标记消息为已读"""
    # 查找消息
    message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")
    
    # 更新消息状态为已读
    message.is_read = True
    db.commit()
    db.refresh(message)
    
    return {
        "id": message.id,
        "sender_id": message.sender_id,
        "receiver_id": message.receiver_id,
        "content": message.content,
        "is_read": message.is_read,
        "created_at": message.created_at
    }
