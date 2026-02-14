from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.character import Character
from app.models.equipment import EquipmentSlot, Equipment

# 创建路由器
router = APIRouter(prefix="/ranking", tags=["ranking"])

# 响应模型
class RankingItem(BaseModel):
    rank: int
    character_id: int
    character_name: str
    user_id: int
    username: str
    level: int
    power: int

class RankingResponse(BaseModel):
    ranking: List[RankingItem]
    personal_rank: int = None

# 计算角色战力
def calculate_character_power(character: Character, db: Session) -> int:
    """
    计算角色战力
    公式: 基础战力 + 等级战力 + 装备战力
    基础战力: 100
    等级战力: 等级 * 10
    装备战力: 所有装备属性之和
    """
    # 基础战力
    base_power = 100
    # 等级战力
    level_power = character.level * 10
    # 装备战力
    equipment_power = 0
    
    # 获取角色已穿戴的装备
    equipment_slots = db.query(EquipmentSlot).filter(EquipmentSlot.character_id == character.id).all()
    for slot in equipment_slots:
        equipment = db.query(Equipment).filter(Equipment.id == slot.equipment_id).first()
        if equipment:
            equipment_power += equipment.attack
            equipment_power += equipment.defense
            equipment_power += equipment.strength
            equipment_power += equipment.agility
            equipment_power += equipment.intelligence
            equipment_power += equipment.vitality
    
    # 总战力
    total_power = base_power + level_power + equipment_power
    return total_power

# 获取等级排行榜
@router.get("/level", response_model=RankingResponse)
def get_level_ranking(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取等级排行榜"""
    # 获取所有角色
    characters = db.query(Character).all()
    
    # 计算每个角色的战力
    character_data = []
    for character in characters:
        power = calculate_character_power(character, db)
        character_data.append({
            "character_id": character.id,
            "character_name": character.name,
            "user_id": character.user_id,
            "username": db.query(User).filter(User.id == character.user_id).first().username,
            "level": character.level,
            "power": power
        })
    
    # 按等级排序，等级相同按经验值排序
    character_data.sort(key=lambda x: (x["level"], x["power"]), reverse=True)
    
    # 生成排行榜
    ranking = []
    for i, data in enumerate(character_data[:100]):
        ranking.append({
            "rank": i + 1,
            "character_id": data["character_id"],
            "character_name": data["character_name"],
            "user_id": data["user_id"],
            "username": data["username"],
            "level": data["level"],
            "power": data["power"]
        })
    
    # 获取个人排名
    personal_rank = None
    user_characters = [data for data in character_data if data["user_id"] == current_user.id]
    if user_characters:
        # 找到用户最高等级的角色
        highest_level_character = max(user_characters, key=lambda x: (x["level"], x["power"]))
        # 找到该角色在排行榜中的位置
        for i, item in enumerate(character_data):
            if item["character_id"] == highest_level_character["character_id"]:
                personal_rank = i + 1
                break
    
    return {
        "ranking": ranking,
        "personal_rank": personal_rank
    }

# 获取战力排行榜
@router.get("/power", response_model=RankingResponse)
def get_power_ranking(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取战力排行榜"""
    # 获取所有角色
    characters = db.query(Character).all()
    
    # 计算每个角色的战力
    character_data = []
    for character in characters:
        power = calculate_character_power(character, db)
        character_data.append({
            "character_id": character.id,
            "character_name": character.name,
            "user_id": character.user_id,
            "username": db.query(User).filter(User.id == character.user_id).first().username,
            "level": character.level,
            "power": power
        })
    
    # 按战力排序
    character_data.sort(key=lambda x: x["power"], reverse=True)
    
    # 生成排行榜
    ranking = []
    for i, data in enumerate(character_data[:100]):
        ranking.append({
            "rank": i + 1,
            "character_id": data["character_id"],
            "character_name": data["character_name"],
            "user_id": data["user_id"],
            "username": data["username"],
            "level": data["level"],
            "power": data["power"]
        })
    
    # 获取个人排名
    personal_rank = None
    user_characters = [data for data in character_data if data["user_id"] == current_user.id]
    if user_characters:
        # 找到用户最高战力的角色
        highest_power_character = max(user_characters, key=lambda x: x["power"])
        # 找到该角色在排行榜中的位置
        for i, item in enumerate(character_data):
            if item["character_id"] == highest_power_character["character_id"]:
                personal_rank = i + 1
                break
    
    return {
        "ranking": ranking,
        "personal_rank": personal_rank
    }
