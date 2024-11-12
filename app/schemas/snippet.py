from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List, Dict
import re

class LanguageBase(BaseModel):
    id: str
    name: str
    extensions: List[str]
    mimeType: str
    aliases: List[str]

    class Config:
        from_attributes = True

class Language(LanguageBase):
    pass

class LanguageResponse(BaseModel):
    success: bool = True
    data: Dict[str, List[LanguageBase]]

class SnippetBase(BaseModel):
    title: str
    code: str
    language: str
    description: Optional[str] = None

class SnippetCreate(BaseModel):
    code: str
    language: str
    title: Optional[str] = None
    description: Optional[str] = None

class SnippetUpdate(SnippetBase):
    pass

class Snippet(SnippetBase):
    id: int
    access_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ShareCodeRequest(BaseModel):
    snippetId: str
    accessCode: Optional[str] = None
    expireTime: str

    @validator('expireTime')
    def validate_expire_time(cls, v):
        # 验证过期时间格式
        pattern = r'^(\d+[hdw]|never)$'
        if not re.match(pattern, v.lower()):
            raise ValueError('Invalid expire time format. Use 1h, 1d, 7d, 30d or never')
        
        if v.lower() != 'never':
            amount = int(v[:-1])
            unit = v[-1].lower()
            
            # 验证时间范围
            if unit == 'h' and (amount < 1 or amount > 24):
                raise ValueError('Hours must be between 1 and 24')
            elif unit == 'd' and (amount < 1 or amount > 30):
                raise ValueError('Days must be between 1 and 30')
            elif unit == 'w' and (amount < 1 or amount > 4):
                raise ValueError('Weeks must be between 1 and 4')
        
        return v.lower()

class ShareCodeResponse(BaseModel):
    success: bool = True
    data: dict

class ShareLinkInfoResponse(BaseModel):
    """分享链接信息响应"""
    success: bool = True
    data: dict = {
        "needAccessCode": bool,
        "expireAt": Optional[datetime],
        "language": str
    }

class ShareLinkContentResponse(BaseModel):
    """分享内容响应"""
    success: bool = True
    data: dict = {
        "code": str,
        "language": str,
        "title": Optional[str],
        "description": Optional[str],
        "createdAt": datetime,
        "expireAt": Optional[datetime]
    }
  