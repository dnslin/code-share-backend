from app.database import SessionLocal
from app.models.snippet import Language
from app.core.languages_config import LANGUAGES_CONFIG

def init_languages():
    db = SessionLocal()
    
    # 清空现有数据
    db.query(Language).delete()
    
    # 从配置文件添加语言
    for category, languages in LANGUAGES_CONFIG.items():
        for lang in languages:
            db_lang = Language(
                id=lang["id"],
                name=lang["name"],
                category=category,
                extensions=lang["extensions"],
                mime_type=lang["mime_type"],
                aliases=lang["aliases"]
            )
            db.add(db_lang)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    init_languages() 