import os
from app.database import Base, engine
from app.init_db import init_languages
from app.core.config import settings

def reset_database():
    # 确保 data 目录存在
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    
    db_path = os.path.join(settings.DATA_DIR, "codeShare.db")
    
    # 删除现有数据库文件
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # 创建新的数据库表
    Base.metadata.create_all(bind=engine)
    
    # 初始化语言数据
    init_languages()

if __name__ == "__main__":
    reset_database()
    print("Database has been reset and initialized successfully!")