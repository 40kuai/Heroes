from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.character import Character
from app.models.task import Task, CharacterTask, TaskStatus
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta

router = APIRouter()


class TaskBase(BaseModel):
    name: str
    description: str
    type: str
    required_level: int = 1
    exp_reward: int = 0
    gold_reward: int = 0
    item_reward: str = ""
    target_count: int = 1
    reset_daily: bool = False


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int

    class Config:
        from_attributes = True


class CharacterTaskBase(BaseModel):
    task_id: int


class CharacterTaskProgress(BaseModel):
    character_task_id: int
    progress: int


class CharacterTaskResponse(BaseModel):
    id: int
    character_id: int
    task_id: int
    status: str
    progress: int
    task: TaskResponse

    class Config:
        from_attributes = True


@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """创建新任务"""
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    # 返回字典格式的数据
    return {
        "id": db_task.id,
        "name": db_task.name,
        "description": db_task.description,
        "type": db_task.type,
        "required_level": db_task.required_level,
        "exp_reward": db_task.exp_reward,
        "gold_reward": db_task.gold_reward,
        "item_reward": db_task.item_reward or "",
        "target_count": db_task.target_count,
        "reset_daily": db_task.reset_daily
    }


@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    """获取所有任务"""
    tasks = db.query(Task).all()
    # 返回字典格式的数据列表
    return [
        {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "type": task.type,
            "required_level": task.required_level,
            "exp_reward": task.exp_reward,
            "gold_reward": task.gold_reward,
            "item_reward": task.item_reward or "",
            "target_count": task.target_count,
            "reset_daily": task.reset_daily
        }
        for task in tasks
    ]


@router.get("/characters/{character_id}/tasks", response_model=List[CharacterTaskResponse])
def get_character_tasks(character_id: int, db: Session = Depends(get_db)):
    """获取角色的所有任务"""
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # 检查并重置日常任务
    reset_daily_tasks(character_id, db)
    
    # 获取或创建角色的任务列表
    update_character_tasks(character_id, db)
    
    # 返回字典格式的数据列表
    return [
        {
            "id": character_task.id,
            "character_id": character_task.character_id,
            "task_id": character_task.task_id,
            "status": character_task.status,
            "progress": character_task.progress,
            "task": {
                "id": character_task.task.id,
                "name": character_task.task.name,
                "description": character_task.task.description,
                "type": character_task.task.type,
                "required_level": character_task.task.required_level,
                "exp_reward": character_task.task.exp_reward,
                "gold_reward": character_task.task.gold_reward,
                "item_reward": character_task.task.item_reward or "",
                "target_count": character_task.task.target_count,
                "reset_daily": character_task.task.reset_daily
            }
        }
        for character_task in character.tasks
    ]


@router.post("/characters/{character_id}/tasks/accept", response_model=CharacterTaskResponse)
def accept_task(character_id: int, task_data: CharacterTaskBase, db: Session = Depends(get_db)):
    """角色接取任务"""
    # 检查角色是否存在
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 检查任务是否存在
    task = db.query(Task).filter(Task.id == task_data.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    # 检查角色等级是否达到任务要求
    if character.level < task.required_level:
        raise HTTPException(status_code=400, detail=f"角色等级不足，需要等级 {task.required_level}")

    # 查找角色的任务
    character_task = db.query(CharacterTask).filter(
        CharacterTask.character_id == character_id,
        CharacterTask.task_id == task_data.task_id
    ).first()

    if not character_task:
        raise HTTPException(status_code=404, detail="任务不可用")

    # 检查任务状态
    if character_task.status != TaskStatus.AVAILABLE:
        raise HTTPException(status_code=400, detail="任务状态不正确")

    # 更新任务状态为已接取
    character_task.status = TaskStatus.ACCEPTED
    character_task.accepted_at = datetime.utcnow()
    db.commit()
    db.refresh(character_task)
    return character_task


@router.post("/characters/{character_id}/tasks/complete", response_model=CharacterTaskResponse)
def complete_task(character_id: int, task_data: CharacterTaskBase, db: Session = Depends(get_db)):
    """角色完成任务"""
    # 检查角色是否存在
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 查找角色的任务
    character_task = db.query(CharacterTask).filter(
        CharacterTask.character_id == character_id,
        CharacterTask.task_id == task_data.task_id
    ).first()

    if not character_task:
        raise HTTPException(status_code=404, detail="任务不存在")

    # 检查任务状态
    if character_task.status != TaskStatus.ACCEPTED:
        raise HTTPException(status_code=400, detail="任务状态不正确")

    # 检查任务进度
    task = character_task.task
    if character_task.progress < task.target_count:
        raise HTTPException(status_code=400, detail="任务进度不足")

    # 更新任务状态为已完成
    character_task.status = TaskStatus.COMPLETED
    character_task.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(character_task)
    return character_task


@router.post("/characters/{character_id}/tasks/reward", response_model=CharacterTaskResponse)
def claim_reward(character_id: int, task_data: CharacterTaskBase, db: Session = Depends(get_db)):
    """角色领取任务奖励"""
    # 检查角色是否存在
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 查找角色的任务
    character_task = db.query(CharacterTask).filter(
        CharacterTask.character_id == character_id,
        CharacterTask.task_id == task_data.task_id
    ).first()

    if not character_task:
        raise HTTPException(status_code=404, detail="任务不存在")

    # 检查任务状态
    if character_task.status != TaskStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="任务尚未完成")

    # 发放奖励
    task = character_task.task
    character.exp += task.exp_reward
    # 这里可以添加金币和物品奖励的逻辑

    # 更新任务状态为已领取奖励
    character_task.status = TaskStatus.REWARDED
    character_task.rewarded_at = datetime.utcnow()
    db.commit()
    db.refresh(character_task)
    return character_task


@router.post("/characters/{character_id}/tasks/progress", response_model=CharacterTaskResponse)
def update_task_progress(character_id: int, progress_data: CharacterTaskProgress, db: Session = Depends(get_db)):
    """更新任务进度"""
    # 检查角色是否存在
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 查找角色的任务
    character_task = db.query(CharacterTask).filter(
        CharacterTask.id == progress_data.character_task_id,
        CharacterTask.character_id == character_id
    ).first()

    if not character_task:
        raise HTTPException(status_code=404, detail="任务不存在")

    # 检查任务状态
    if character_task.status not in [TaskStatus.ACCEPTED, TaskStatus.COMPLETED]:
        raise HTTPException(status_code=400, detail="任务状态不正确")

    # 更新任务进度
    task = character_task.task
    character_task.progress = min(progress_data.progress, task.target_count)
    
    # 如果进度达到目标，自动完成任务
    if character_task.progress >= task.target_count and character_task.status == TaskStatus.ACCEPTED:
        character_task.status = TaskStatus.COMPLETED
        character_task.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(character_task)
    return character_task


# 辅助函数：更新角色的任务列表
def update_character_tasks(character_id: int, db: Session):
    """为角色创建可用的任务记录"""
    # 获取角色
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        return

    # 获取所有适合角色等级的任务
    available_tasks = db.query(Task).filter(Task.required_level <= character.level).all()

    for task in available_tasks:
        # 检查角色是否已有该任务
        existing_task = db.query(CharacterTask).filter(
            CharacterTask.character_id == character_id,
            CharacterTask.task_id == task.id
        ).first()

        if not existing_task:
            # 创建新的任务记录
            new_character_task = CharacterTask(
                character_id=character_id,
                task_id=task.id,
                status=TaskStatus.AVAILABLE,
                progress=0
            )
            db.add(new_character_task)

    db.commit()


# 辅助函数：重置日常任务
def reset_daily_tasks(character_id: int, db: Session):
    """重置角色的日常任务"""
    # 获取角色的所有日常任务
    character_tasks = db.query(CharacterTask).join(Task).filter(
        CharacterTask.character_id == character_id,
        Task.type == "daily",
        Task.reset_daily == True
    ).all()

    for character_task in character_tasks:
        # 检查是否需要重置（24小时前领取奖励）
        if character_task.rewarded_at:
            time_since_reward = datetime.utcnow() - character_task.rewarded_at
            if time_since_reward >= timedelta(hours=24):
                # 重置任务
                character_task.status = TaskStatus.AVAILABLE
                character_task.progress = 0
                character_task.accepted_at = None
                character_task.completed_at = None
                character_task.rewarded_at = None

    db.commit()
