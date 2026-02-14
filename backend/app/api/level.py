from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.character import Character

# 创建路由器
router = APIRouter(prefix="/api/level", tags=["level"])

# 请求和响应模型
class ExpGain(BaseModel):
    character_id: int
    exp: int

class LevelResponse(BaseModel):
    character_id: int
    name: str
    level: int
    exp: int
    next_level_exp: int
    level_up: bool
    new_level: int = None

# 计算升级所需经验值
def calculate_next_level_exp(current_level: int) -> int:
    """
    计算升级所需经验值
    公式: 基础经验值 * 等级因子
    基础经验值: 1000
    等级因子: 1.5 ^ (等级-1)
    """
    base_exp = 1000
    level_factor = 1.5 ** (current_level - 1)
    return int(base_exp * level_factor)

# 根据职业类型获取属性成长系数
def get_class_growth_bonus(class_type: str) -> Dict[str, float]:
    """
    根据职业类型获取属性成长系数
    """
    growth_bonuses = {
        "warrior": {"strength": 1.5, "vitality": 1.3, "agility": 0.8, "intelligence": 0.5},
        "mage": {"intelligence": 1.5, "agility": 0.8, "vitality": 0.7, "strength": 0.5},
        "archer": {"agility": 1.5, "strength": 1.0, "intelligence": 0.7, "vitality": 0.8},
        "thief": {"agility": 1.4, "intelligence": 0.9, "strength": 0.9, "vitality": 0.8},
        "priest": {"intelligence": 1.3, "vitality": 1.1, "strength": 0.6, "agility": 0.7}
    }
    return growth_bonuses.get(class_type.lower(), {"strength": 1.0, "agility": 1.0, "intelligence": 1.0, "vitality": 1.0})

# 计算属性成长值
def calculate_attribute_growth(current_level: int, base_growth: float, class_bonus: float) -> int:
    """
    计算属性成长值
    公式: 基础成长值 * 等级因子 * 职业系数
    """
    base_growth_value = 2
    level_factor = 1 + (current_level - 1) * 0.05  # 等级越高，成长越高
    total_growth = base_growth_value * level_factor * class_bonus
    return int(total_growth)

# 更新衍生属性
def update_derived_attributes(character: Character):
    """
    更新衍生属性
    """
    # 生命值 = 基础值(100) + 体力 * 10
    character.hp = 100 + character.vitality * 10
    # 魔法值 = 基础值(50) + 智力 * 8
    character.mp = 50 + character.intelligence * 8
    # 攻击力 = 基础值(10) + 力量 * 2 + 敏捷 * 0.5
    character.attack = 10 + character.strength * 2 + character.agility * 0.5
    # 防御力 = 基础值(5) + 体力 * 1 + 力量 * 0.5
    character.defense = 5 + character.vitality * 1 + character.strength * 0.5

# 处理等级提升
def handle_level_up(character: Character, exp_gained: int) -> Dict:
    """
    处理角色经验值获取和等级提升
    """
    original_level = character.level
    character.exp += exp_gained
    level_up = False
    new_level = original_level
    
    # 检查是否可以升级
    while character.exp >= calculate_next_level_exp(character.level):
        character.level += 1
        character.exp -= calculate_next_level_exp(character.level - 1)
        level_up = True
        new_level = character.level
        
        # 获取职业成长系数
        class_bonus = get_class_growth_bonus(character.class_type)
        
        # 增加基础属性
        character.strength += calculate_attribute_growth(character.level, 1.0, class_bonus.get("strength", 1.0))
        character.agility += calculate_attribute_growth(character.level, 1.0, class_bonus.get("agility", 1.0))
        character.intelligence += calculate_attribute_growth(character.level, 1.0, class_bonus.get("intelligence", 1.0))
        character.vitality += calculate_attribute_growth(character.level, 1.0, class_bonus.get("vitality", 1.0))
        
        # 更新衍生属性
        update_derived_attributes(character)
        
        # 限制等级上限为100级
        if character.level >= 100:
            character.exp = 0
            break
    
    return {
        "level_up": level_up,
        "new_level": new_level if level_up else None
    }

# 获取角色等级信息
@router.get("/{character_id}", response_model=Dict)
def get_character_level(character_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取角色等级信息"""
    character = db.query(Character).filter(Character.id == character_id, Character.user_id == current_user.id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    next_level_exp = calculate_next_level_exp(character.level)
    
    return {
        "character_id": character.id,
        "name": character.name,
        "level": character.level,
        "exp": character.exp,
        "next_level_exp": next_level_exp,
        "exp_percentage": min(100, (character.exp / next_level_exp) * 100),
        # 属性信息
        "strength": character.strength,
        "agility": character.agility,
        "intelligence": character.intelligence,
        "vitality": character.vitality,
        "hp": character.hp,
        "mp": character.mp,
        "attack": character.attack,
        "defense": character.defense
    }

# 获取经验值
def gain_exp(character_id: int, exp: int, db: Session, current_user: User) -> Character:
    """
    为角色添加经验值并处理等级提升
    """
    character = db.query(Character).filter(Character.id == character_id, Character.user_id == current_user.id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 检查经验值获取限制（每日经验值获取上限为10000）
    # 这里简化处理，实际应该在数据库中记录每日经验值获取量
    if exp > 5000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="单次经验值获取不能超过5000"
        )
    
    # 处理等级提升
    result = handle_level_up(character, exp)
    
    db.commit()
    db.refresh(character)
    
    return character

# 角色获取经验值
@router.post("/gain-exp", response_model=LevelResponse)
def character_gain_exp(exp_gain: ExpGain, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """角色获取经验值"""
    character = gain_exp(exp_gain.character_id, exp_gain.exp, db, current_user)
    
    next_level_exp = calculate_next_level_exp(character.level)
    
    return {
        "character_id": character.id,
        "name": character.name,
        "level": character.level,
        "exp": character.exp,
        "next_level_exp": next_level_exp,
        "level_up": character.level > 1,
        "new_level": character.level
    }

# 批量获取角色等级信息
@router.get("/", response_model=Dict)
def get_characters_level(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取当前用户所有角色的等级信息"""
    characters = db.query(Character).filter(Character.user_id == current_user.id).all()
    
    result = []
    for character in characters:
        next_level_exp = calculate_next_level_exp(character.level)
        result.append({
            "character_id": character.id,
            "name": character.name,
            "level": character.level,
            "exp": character.exp,
            "next_level_exp": next_level_exp,
            "exp_percentage": min(100, (character.exp / next_level_exp) * 100),
            # 属性信息
            "strength": character.strength,
            "agility": character.agility,
            "intelligence": character.intelligence,
            "vitality": character.vitality,
            "hp": character.hp,
            "mp": character.mp,
            "attack": character.attack,
            "defense": character.defense
        })
    
    return {"characters": result}
