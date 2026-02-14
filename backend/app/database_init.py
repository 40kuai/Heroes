from app.database import engine, Base
from app.models import user, character, skill, equipment, task, social, shop  # 导入所有模型，确保它们被注册

# 创建所有表
def init_db():
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功！")
