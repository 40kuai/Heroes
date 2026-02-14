from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.character import Character
from app.models.equipment import Equipment, EquipmentSlot

# 创建路由器
router = APIRouter(prefix="/equipment", tags=["equipment"])

# 请求和响应模型
class EquipmentCreate(BaseModel):
    name: str
    type: str
    level: int
    rarity: str
    attack: int = 0
    defense: int = 0
    strength: int = 0
    agility: int = 0
    intelligence: int = 0
    vitality: int = 0
    durability: int = 100
    price: int = 0

class EquipmentResponse(BaseModel):
    id: int
    name: str
    type: str
    level: int
    rarity: str
    attack: int
    defense: int
    strength: int
    agility: int
    intelligence: int
    vitality: int
    durability: int
    price: int

    class Config:
        from_attributes = True

class EquipmentSlotCreate(BaseModel):
    character_id: int
    equipment_id: int
    slot_type: str

class EquipmentSlotResponse(BaseModel):
    id: int
    character_id: int
    equipment_id: int
    slot_type: str
    equipment: EquipmentResponse

    class Config:
        from_attributes = True

# 创建装备
@router.post("/", response_model=EquipmentResponse)
def create_equipment(equipment: EquipmentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """创建新装备"""
    # 创建装备
    db_equipment = Equipment(
        name=equipment.name,
        type=equipment.type,
        level=equipment.level,
        rarity=equipment.rarity,
        attack=equipment.attack,
        defense=equipment.defense,
        strength=equipment.strength,
        agility=equipment.agility,
        intelligence=equipment.intelligence,
        vitality=equipment.vitality,
        durability=equipment.durability,
        price=equipment.price
    )
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

# 获取装备列表
@router.get("/", response_model=List[EquipmentResponse])
def get_equipment_list(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取装备列表"""
    equipment = db.query(Equipment).all()
    return equipment

# 获取单个装备信息
@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment(equipment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取单个装备信息"""
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="装备不存在"
        )
    return equipment

# 穿戴装备
@router.post("/equip", response_model=EquipmentSlotResponse)
def equip_equipment(slot_data: EquipmentSlotCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """穿戴装备"""
    # 检查角色是否存在且属于当前用户
    character = db.query(Character).filter(Character.id == slot_data.character_id, Character.user_id == current_user.id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 检查装备是否存在
    equipment = db.query(Equipment).filter(Equipment.id == slot_data.equipment_id).first()
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="装备不存在"
        )
    
    # 检查装备等级是否不超过角色等级
    if equipment.level > character.level:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="装备等级不能超过角色等级"
        )
    
    # 检查槽位类型是否有效
    valid_slot_types = ["武器", "头盔", "胸甲", "手套", "靴子", "饰品1", "饰品2"]
    if slot_data.slot_type not in valid_slot_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的槽位类型"
        )
    
    # 检查该槽位是否已穿戴装备
    existing_slot = db.query(EquipmentSlot).filter(
        EquipmentSlot.character_id == slot_data.character_id,
        EquipmentSlot.slot_type == slot_data.slot_type
    ).first()
    
    if existing_slot:
        # 如果已穿戴装备，先卸下
        db.delete(existing_slot)
        db.commit()
    
    # 创建新的装备槽位记录
    new_slot = EquipmentSlot(
        character_id=slot_data.character_id,
        equipment_id=slot_data.equipment_id,
        slot_type=slot_data.slot_type
    )
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    
    # 加载装备信息
    db.refresh(new_slot.equipment)
    
    return new_slot

# 卸下装备
@router.delete("/unequip/{slot_id}")
def unequip_equipment(slot_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """卸下装备"""
    # 检查装备槽位是否存在
    slot = db.query(EquipmentSlot).filter(EquipmentSlot.id == slot_id).first()
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="装备槽位不存在"
        )
    
    # 检查角色是否属于当前用户
    character = db.query(Character).filter(Character.id == slot.character_id, Character.user_id == current_user.id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 删除装备槽位记录
    db.delete(slot)
    db.commit()
    
    return {"message": "装备卸下成功"}

# 获取角色已穿戴的装备
@router.get("/character/{character_id}", response_model=List[EquipmentSlotResponse])
def get_character_equipment(character_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取角色已穿戴的装备"""
    # 检查角色是否存在且属于当前用户
    character = db.query(Character).filter(Character.id == character_id, Character.user_id == current_user.id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 获取角色已穿戴的装备
    slots = db.query(EquipmentSlot).filter(EquipmentSlot.character_id == character_id).all()
    
    # 加载装备信息
    for slot in slots:
        db.refresh(slot.equipment)
    
    return slots
