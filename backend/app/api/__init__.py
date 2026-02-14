from fastapi import APIRouter
from app.api import user, character, level, equipment, ranking

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
