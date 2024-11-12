import os
from app.database import Base, engine
from app.init_db import init_languages

def reset_database():
    # 删除现有数据库文件
    if os.path.exists("codeShare.db"):
        os.remove("codeShare.db")
    
    # 创建新的数据库表
    Base.metadata.create_all(bind=engine)
    
    # 初始化语言数据
    init_languages()

if __name__ == "__main__":
    reset_database()
    print("Database has been reset and initialized successfully!") 