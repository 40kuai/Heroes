from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# JWT配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 密码加密上下文
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# 密码加密
def get_password_hash(password):
    """获取密码的哈希值"""
    # 截断密码，确保不超过72字节
    password = password[:72]
    return pwd_context.hash(password)

# 密码验证
def verify_password(plain_password, hashed_password):
    """验证密码是否正确"""
    # 截断密码，确保不超过72字节，与加密时处理一致
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)

# 创建访问令牌
def create_access_token(data: dict, expires_delta: timedelta = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 验证访问令牌
def verify_token(token: str):
    """验证访问令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
        return {"user_id": user_id}
    except JWTError:
        return None
