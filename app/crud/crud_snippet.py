from sqlalchemy.orm import Session
from sqlalchemy import and_
import uuid
import secrets
from datetime import datetime, timedelta
from typing import Optional, Tuple
from app.models.snippet import Snippet
from app.schemas.snippet import ShareCodeRequest

def generate_share_link() -> str:
    """生成随机的分享链接"""
    return secrets.token_urlsafe(8)

def parse_expire_time(expire_time: str) -> Optional[datetime]:
    """解析过期时间字符串，返回具体的过期时间"""
    if expire_time == 'never':
        return None
        
    amount = int(expire_time[:-1])
    unit = expire_time[-1]
    
    now = datetime.utcnow()
    
    if unit == 'h':
        return now + timedelta(hours=amount)
    elif unit == 'd':
        return now + timedelta(days=amount)
    elif unit == 'w':
        return now + timedelta(weeks=amount)
    
    raise ValueError(f"Unsupported expire time format: {expire_time}")

def create_share_link(
    db: Session, 
    share_request: ShareCodeRequest
) -> Tuple[Optional[Snippet], Optional[str]]:
    """创建分享链接，如果已存在则更新"""
    # 检查代码片段是否存在
    snippet = db.query(Snippet).filter(
        Snippet.sequence == share_request.snippetId
    ).first()
    
    if not snippet:
        return None, "Snippet not found"
    
    # 生成新的分享链接，覆盖旧的
    share_link = generate_share_link()
    expire_at = parse_expire_time(share_request.expireTime)
    
    # 更新代码片段
    snippet.share_link = share_link
    snippet.access_code = share_request.accessCode
    snippet.expire_at = expire_at
    snippet.shared_at = datetime.utcnow()
    
    db.commit()
    db.refresh(snippet)
    
    return snippet, None

def get_shared_snippet(
    db: Session, 
    share_link: str, 
    access_code: Optional[str] = None
) -> Tuple[Optional[Snippet], Optional[str]]:
    """获取分享的代码片段"""
    # 构建查询条件
    conditions = [Snippet.share_link == share_link]
    
    # 如果设置了访问码，需要验证
    if access_code:
        conditions.append(Snippet.access_code == access_code)
    
    snippet = db.query(Snippet).filter(and_(*conditions)).first()
    
    if not snippet:
        return None, "Shared snippet not found"
    
    # 检查是否过期
    if snippet.expire_at and snippet.expire_at < datetime.utcnow():
        return None, "Share link has expired"
    
    # 如果需要访问码但未提供
    if snippet.access_code and not access_code:
        return None, "Access code required"
    
    return snippet, None

def get_share_link_info(
    db: Session,
    share_link: str
) -> Tuple[Optional[dict], Optional[str]]:
    """获取分享链接的基本信息"""
    snippet = db.query(Snippet).filter(Snippet.share_link == share_link).first()
    
    if not snippet:
        return None, "Share link not found"
    
    # 检查是否过期
    if snippet.expire_at and snippet.expire_at < datetime.utcnow():
        return None, "Share link has expired"
    
    return {
        "needAccessCode": bool(snippet.access_code),
        "expireAt": snippet.expire_at,
        "language": snippet.language
    }, None

def get_share_link_content(
    db: Session,
    share_link: str,
    access_code: Optional[str] = None
) -> Tuple[Optional[Snippet], Optional[str]]:
    """获取分享内容"""
    snippet = db.query(Snippet).filter(Snippet.share_link == share_link).first()
    
    if not snippet:
        return None, "Share link not found"
    
    # 检查是否过期
    if snippet.expire_at and snippet.expire_at < datetime.utcnow():
        return None, "Share link has expired"
    
    # 验证访问码
    if snippet.access_code:
        if not access_code:
            return None, "Access code required"
        if access_code != snippet.access_code:
            return None, "Invalid access code"
    
    return snippet, None