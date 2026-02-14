from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.jwt import verify_token
from app.models.user import User

# OAuth2密码Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

# 获取当前用户
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 验证令牌
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    # 获取用户ID
    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    
    # 从数据库中获取用户
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

# 获取当前活跃用户
def get_current_active_user(current_user: User = Depends(get_current_user)):
    """获取当前活跃用户"""
    # 这里可以添加额外的检查，比如用户是否被禁用
    return current_user
