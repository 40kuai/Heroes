from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.character import Character
from app.models.skill import Skill, CharacterSkill
from pydantic import BaseModel
from typing import List

router = APIRouter()


class SkillBase(BaseModel):
    name: str
    description: str
    type: str
    rarity: str
    base_damage: float = 0.0
    base_defense: float = 0.0
    base_healing: float = 0.0
    cooldown: int = 0
    required_level: int = 1
    mana_cost: int = 0


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: int

    class Config:
        from_attributes = True


class CharacterSkillBase(BaseModel):
    skill_id: int


class CharacterSkillUpgrade(BaseModel):
    character_skill_id: int


class CharacterSkillResponse(BaseModel):
    id: int
    character_id: int
    skill_id: int
    skill_level: int
    experience: int
    skill: SkillResponse

    class Config:
        from_attributes = True


@router.post("/skills", response_model=SkillResponse)
def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    """创建新技能"""
    db_skill = Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@router.get("/skills", response_model=List[SkillResponse])
def get_skills(db: Session = Depends(get_db)):
    """获取所有技能"""
    return db.query(Skill).all()


@router.get("/characters/{character_id}/skills", response_model=List[CharacterSkillResponse])
def get_character_skills(character_id: int, db: Session = Depends(get_db)):
    """获取角色的所有技能"""
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="角色不存在")
    return character.skills


@router.post("/characters/{character_id}/skills", response_model=CharacterSkillResponse)
def learn_skill(character_id: int, skill_data: CharacterSkillBase, db: Session = Depends(get_db)):
    """角色学习技能"""
    # 检查角色是否存在
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 检查技能是否存在
    skill = db.query(Skill).filter(Skill.id == skill_data.skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="技能不存在")

    # 检查角色等级是否达到技能要求
    if character.level < skill.required_level:
        raise HTTPException(status_code=400, detail=f"角色等级不足，需要等级 {skill.required_level}")

    # 检查角色是否已经学习了该技能
    existing_skill = db.query(CharacterSkill).filter(
        CharacterSkill.character_id == character_id,
        CharacterSkill.skill_id == skill_data.skill_id
    ).first()
    if existing_skill:
        raise HTTPException(status_code=400, detail="角色已经学习了该技能")

    # 创建新的技能学习记录
    character_skill = CharacterSkill(
        character_id=character_id,
        skill_id=skill_data.skill_id,
        skill_level=1,
        experience=0
    )
    db.add(character_skill)
    db.commit()
    db.refresh(character_skill)
    return character_skill


@router.post("/character-skills/upgrade", response_model=CharacterSkillResponse)
def upgrade_skill(upgrade_data: CharacterSkillUpgrade, db: Session = Depends(get_db)):
    """升级角色技能"""
    # 检查技能学习记录是否存在
    character_skill = db.query(CharacterSkill).filter(
        CharacterSkill.id == upgrade_data.character_skill_id
    ).first()
    if not character_skill:
        raise HTTPException(status_code=404, detail="技能学习记录不存在")

    # 获取角色信息
    character = db.query(Character).filter(
        Character.id == character_skill.character_id
    ).first()
    if not character:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 检查技能等级是否超过角色等级
    if character_skill.skill_level >= character.level:
        raise HTTPException(status_code=400, detail="技能等级不能超过角色等级")

    # 升级技能
    character_skill.skill_level += 1
    character_skill.experience = 0  # 重置经验值
    db.commit()
    db.refresh(character_skill)
    return character_skill
