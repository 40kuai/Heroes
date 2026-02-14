from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    class_type = Column(String(50), nullable=True)  # 职业类型
    # 基础属性
    strength = Column(Integer, default=10)  # 力量
    agility = Column(Integer, default=10)   # 敏捷
    intelligence = Column(Integer, default=10)  # 智力
    vitality = Column(Integer, default=10)  # 体力
    # 衍生属性
    hp = Column(Integer, default=100)  # 生命值
    mp = Column(Integer, default=50)   # 魔法值
    attack = Column(Integer, default=10)  # 攻击力
    defense = Column(Integer, default=5)   # 防御力
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    user = relationship("User", backref="characters")
