from sqlalchemy.orm import Session
import uuid
from datetime import datetime, timedelta
from typing import Optional
from app.models.snippet import Snippet, Language
from app.schemas.snippet import SnippetCreate, SnippetUpdate, LanguageBase

def parse_expire_time(expire_time: str) -> Optional[datetime]:
    """解析过期时间字符串，返回具体的过期时间"""
    if expire_time.lower() == 'never':
        return None
        
    # 解析数字和单位
    amount = int(expire_time[:-1])
    unit = expire_time[-1].lower()
    
    now = datetime.utcnow()
    
    if unit == 'd':
        return now + timedelta(days=amount)
    elif unit == 'h':
        return now + timedelta(hours=amount)
    elif unit == 'w':
        return now + timedelta(weeks=amount)
    elif unit == 'm':
        return now + timedelta(days=amount * 30)
    else:
        raise ValueError(f"Unsupported expire time format: {expire_time}")

def get_snippet(db: Session, snippet_id: int):
    snippet = db.query(Snippet).filter(Snippet.id == snippet_id).first()
    if snippet and snippet.expire_at:
        if snippet.expire_at < datetime.utcnow():
            return None
    return snippet

def get_snippet_by_access_code(db: Session, access_code: str):
    snippet = db.query(Snippet).filter(Snippet.access_code == access_code).first()
    if snippet and snippet.expire_at:
        if snippet.expire_at < datetime.utcnow():
            return None
    return snippet

def create_snippet(db: Session, snippet: SnippetCreate, expire_time: Optional[str] = None):
    snippet_data = snippet.model_dump()
    if expire_time:
        snippet_data['expire_at'] = parse_expire_time(expire_time)
        
    db_snippet = Snippet(**snippet_data)
    db.add(db_snippet)
    db.commit()
    db.refresh(db_snippet)
    return db_snippet

def update_snippet(db: Session, snippet_id: int, snippet: SnippetUpdate):
    db_snippet = get_snippet(db, snippet_id)
    if db_snippet:
        for key, value in snippet.model_dump().items():
            setattr(db_snippet, key, value)
        db.commit()
        db.refresh(db_snippet)
    return db_snippet

def create_share_code(db: Session, snippet_id: int, expire_time: Optional[str] = None):
    db_snippet = get_snippet(db, snippet_id)
    if db_snippet:
        db_snippet.access_code = str(uuid.uuid4())
        if expire_time:
            db_snippet.expire_at = parse_expire_time(expire_time)
        db.commit()
        db.refresh(db_snippet)
    return db_snippet

def get_languages(db: Session):
    languages = db.query(Language).all()
    
    categorized_languages = {}
    for lang in languages:
        category = lang.category
        if category not in categorized_languages:
            categorized_languages[category] = []
            
        language_data = LanguageBase(
            id=lang.id,
            name=lang.name,
            extensions=lang.extensions.split(','),
            mimeType=lang.mime_type,
            aliases=lang.aliases.split(',')
        )
        categorized_languages[category].append(language_data)
    
    return categorized_languages

def cleanup_expired_snippets(db: Session):
    """清理过期的代码片段"""
    now = datetime.utcnow()
    expired_snippets = (
        db.query(Snippet)
        .filter(Snippet.expire_at.isnot(None))
        .filter(Snippet.expire_at < now)
        .all()
    )
    
    for snippet in expired_snippets:
        db.delete(snippet)
    
    db.commit()
    return len(expired_snippets)