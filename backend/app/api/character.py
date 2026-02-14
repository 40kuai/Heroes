from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.character import Character

# 创建路由器
router = APIRouter(prefix="/character", tags=["character"])

# 请求和响应模型
class CharacterCreate(BaseModel):
    name: str
    class_type: str

class CharacterUpdate(BaseModel):
    name: Optional[str] = None

class CharacterResponse(BaseModel):
    id: int
    name: str
    user_id: int
    level: int
    exp: int
    class_type: Optional[str] = None
    # 基础属性
    strength: int
    agility: int
    intelligence: int
    vitality: int
    # 衍生属性
    hp: int
    mp: int
    attack: int
    defense: int

    class Config:
        from_attributes = True

# 角色创建
@router.post("/", response_model=CharacterResponse)
def create_character(character: CharacterCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """创建新角色"""
    # 检查角色数量限制（每个用户最多3个角色）
    character_count = db.query(Character).filter(Character.user_id == current_user.id).count()
    if character_count >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="每个用户最多只能创建3个角色"
        )
    
    # 检查角色名称是否已存在
    existing_character = db.query(Character).filter(Character.name == character.name, Character.user_id == current_user.id).first()
    if existing_character:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="角色名称已存在"
        )
    
    # 初始化角色属性
    class_initial_attributes = {
        "战士": {"strength": 15, "agility": 10, "intelligence": 8, "vitality": 12},
        "法师": {"strength": 8, "agility": 10, "intelligence": 15, "vitality": 8},
        "射手": {"strength": 10, "agility": 15, "intelligence": 10, "vitality": 10},
        "刺客": {"strength": 12, "agility": 14, "intelligence": 10, "vitality": 9},
        "牧师": {"strength": 9, "agility": 9, "intelligence": 13, "vitality": 11}
    }
    
    # 获取职业初始属性
    initial_attrs = class_initial_attributes.get(character.class_type, {"strength": 10, "agility": 10, "intelligence": 10, "vitality": 10})
    
    # 创建新角色
    db_character = Character(
        name=character.name,
        user_id=current_user.id,
        level=1,
        exp=0,
        class_type=character.class_type,
        # 基础属性
        strength=initial_attrs["strength"],
        agility=initial_attrs["agility"],
        intelligence=initial_attrs["intelligence"],
        vitality=initial_attrs["vitality"],
        # 衍生属性
        hp=100 + initial_attrs["vitality"] * 10,
        mp=50 + initial_attrs["intelligence"] * 8,
        attack=10 + initial_attrs["strength"] * 2 + initial_attrs["agility"] * 0.5,
        defense=5 + initial_attrs["vitality"] * 1 + initial_attrs["strength"] * 0.5
    )
    
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    
    # 返回字典格式的数据
    return {
        "id": db_character.id,
        "name": db_character.name,
        "user_id": db_character.user_id,
        "level": db_character.level,
        "exp": db_character.exp,
        "class_type": db_character.class_type,
        "strength": db_character.strength,
        "agility": db_character.agility,
        "intelligence": db_character.intelligence,
        "vitality": db_character.vitality,
        "hp": db_character.hp,
        "mp": db_character.mp,
        "attack": db_character.attack,
        "defense": db_character.defense
    }

# 获取用户的所有角色
@router.get("/", response_model=List[CharacterResponse])
def get_characters(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取当前用户的所有角色"""
    characters = db.query(Character).filter(Character.user_id == current_user.id).all()
    # 返回字典格式的数据列表
    return [
        {
            "id": character.id,
            "name": character.name,
            "user_id": character.user_id,
            "level": character.level,
            "exp": character.exp,
            "class_type": character.class_type,
            "strength": character.strength,
            "agility": character.agility,
            "intelligence": character.intelligence,
            "vitality": character.vitality,
            "hp": character.hp,
            "mp": character.mp,
            "attack": character.attack,
            "defense": character.defense
        }
        for character in characters
    ]

# 获取单个角色信息
@router.get("/{character_id}", response_model=CharacterResponse)
def get_character(character_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取单个角色信息"""
    character = db.query(Character).filter(Character.id == character_id, Character.user_id == current_user.id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    return character

# 更新角色信息
@router.put("/{character_id}", response_model=CharacterResponse)
def update_character(character_id: int, character_update: CharacterUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """更新角色信息"""
    character = db.query(Character).filter(Character.id == character_id, Character.user_id == current_user.id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 更新角色名称
    if character_update.name:
        # 检查角色名称是否已存在
        existing_character = db.query(Character).filter(Character.name == character_update.name, Character.user_id == current_user.id, Character.id != character_id).first()
        if existing_character:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="角色名称已存在"
            )
        character.name = character_update.name
    
    db.commit()
    db.refresh(character)
    return character

# 删除角色
@router.delete("/{character_id}")
def delete_character(character_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """删除角色"""
    character = db.query(Character).filter(Character.id == character_id, Character.user_id == current_user.id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    db.delete(character)
    db.commit()
    return {"message": "角色删除成功"}

# 获取角色数量
@router.get("/count", response_model=dict)
def get_character_count(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取当前用户的角色数量"""
    count = db.query(Character).filter(Character.user_id == current_user.id).count()
    return {"count": count, "limit": 3}
