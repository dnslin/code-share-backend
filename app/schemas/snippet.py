from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

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
    code: str
    language: str
    expireTime: str

class ShareCodeResponse(BaseModel):
    success: bool = True
    data: dict
  