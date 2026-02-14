from fastapi import APIRouter
from app.api import user, character, level, equipment, ranking, skill, task, social, shop

# 创建主路由器
router = APIRouter()

# 包含用户路由
router.include_router(user.router)

# 包含角色路由
router.include_router(character.router)

# 包含等级路由
router.include_router(level.router)

# 包含装备路由
router.include_router(equipment.router)

# 包含排行榜路由
router.include_router(ranking.router)

# 包含技能路由
router.include_router(skill.router)

# 包含任务路由
router.include_router(task.router)

# 包含社交路由
router.include_router(social.router)

# 包含商城路由
router.include_router(shop.router)
