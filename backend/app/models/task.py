from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class TaskType(str, enum.Enum):
    MAIN = "main"
    DAILY = "daily"
    SIDE = "side"


class TaskStatus(str, enum.Enum):
    AVAILABLE = "available"
    ACCEPTED = "accepted"
    COMPLETED = "completed"
    REWARDED = "rewarded"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    type = Column(SQLEnum(TaskType), nullable=False)
    required_level = Column(Integer, default=1)
    exp_reward = Column(Integer, default=0)
    gold_reward = Column(Integer, default=0)
    item_reward = Column(String, nullable=True)
    target_count = Column(Integer, default=1)
    reset_daily = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship with CharacterTask
    character_tasks = relationship("CharacterTask", back_populates="task")


class CharacterTask(Base):
    __tablename__ = "character_tasks"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.AVAILABLE)
    progress = Column(Integer, default=0)
    accepted_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    rewarded_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    character = relationship("Character", back_populates="tasks")
    task = relationship("Task", back_populates="character_tasks")
