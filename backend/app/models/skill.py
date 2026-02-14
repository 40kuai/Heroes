from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class SkillType(str, enum.Enum):
    ATTACK = "attack"
    DEFENSE = "defense"
    SUPPORT = "support"
    SPECIAL = "special"


class SkillRarity(str, enum.Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    type = Column(SQLEnum(SkillType))
    rarity = Column(SQLEnum(SkillRarity))
    base_damage = Column(Float, default=0.0)
    base_defense = Column(Float, default=0.0)
    base_healing = Column(Float, default=0.0)
    cooldown = Column(Integer, default=0)
    required_level = Column(Integer, default=1)
    mana_cost = Column(Integer, default=0)

    # Relationship with CharacterSkill
    character_skills = relationship("CharacterSkill", back_populates="skill")


class CharacterSkill(Base):
    __tablename__ = "character_skills"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    skill_level = Column(Integer, default=1)
    experience = Column(Integer, default=0)

    # Relationships
    character = relationship("Character", back_populates="skills")
    skill = relationship("Skill", back_populates="character_skills")
