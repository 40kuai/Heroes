from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # 装备类型：武器、防具、饰品等
    level = Column(Integer, default=1)  # 装备等级
    rarity = Column(String(50), nullable=False)  # 装备稀有度：普通、优秀、稀有、史诗、传说
    # 属性加成
    attack = Column(Integer, default=0)  # 攻击力加成
    defense = Column(Integer, default=0)  # 防御力加成
    strength = Column(Integer, default=0)  # 力量加成
    agility = Column(Integer, default=0)  # 敏捷加成
    intelligence = Column(Integer, default=0)  # 智力加成
    vitality = Column(Integer, default=0)  # 体力加成
    # 其他属性
    durability = Column(Integer, default=100)  # 耐久度
    price = Column(Integer, default=0)  # 价格
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    # 装备和角色的多对多关系需要通过中间表实现
    
class EquipmentSlot(Base):
    __tablename__ = "equipment_slots"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    slot_type = Column(String(50), nullable=False)  # 槽位类型：武器、头盔、胸甲、手套、靴子、饰品1、饰品2
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    character = relationship("Character", backref="equipment_slots")
    equipment = relationship("Equipment", backref="equipment_slots")
