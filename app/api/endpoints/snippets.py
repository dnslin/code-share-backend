from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.crud import crud_snippet
from app.schemas.snippet import (
    Snippet, SnippetCreate, SnippetUpdate,
    Language, ShareCodeRequest, ShareCodeResponse,
    LanguageResponse
)
from app.database import get_db

router = APIRouter()

@router.get("/languages", response_model=LanguageResponse)
def get_languages(db: Session = Depends(get_db)):
    languages = crud_snippet.get_languages(db)
    return LanguageResponse(success=True, data=languages)

@router.get("/shared/{access_code}", response_model=Snippet)
def get_shared_code(access_code: str, db: Session = Depends(get_db)):
    db_snippet = crud_snippet.get_snippet_by_access_code(db, access_code)
    if db_snippet is None:
        raise HTTPException(status_code=404, detail="Shared code not found")
    return db_snippet

@router.post("/share", response_model=ShareCodeResponse)
def share_code(
    share_request: ShareCodeRequest, 
    db: Session = Depends(get_db)
):
    # 创建新的代码片段
    snippet = SnippetCreate(
        code=share_request.code,
        language=share_request.language,
        title=f"Shared code - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    # 保存代码片段并设置过期时间
    db_snippet = crud_snippet.create_snippet(
        db=db, 
        snippet=snippet,
        expire_time=share_request.expireTime
    )
    
    # 生成访问代码
    db_snippet = crud_snippet.create_share_code(
        db, 
        db_snippet.id,
        expire_time=share_request.expireTime
    )
    
    if db_snippet is None:
        raise HTTPException(status_code=404, detail="Failed to create shared code")
    
    # 计算人类可读的过期时间
    expire_at = db_snippet.expire_at.isoformat() if db_snippet.expire_at else 'never'
    
    return ShareCodeResponse(
        success=True,
        data={
            "id": db_snippet.id,
            "accessCode": db_snippet.access_code,
            "expireTime": expire_at
        }
    )

@router.post("/", response_model=Snippet)
def create_snippet(snippet: SnippetCreate, db: Session = Depends(get_db)):
    return crud_snippet.create_snippet(db=db, snippet=snippet)

@router.get("/{snippet_id}", response_model=Snippet)
def get_snippet(snippet_id: int, db: Session = Depends(get_db)):
    db_snippet = crud_snippet.get_snippet(db, snippet_id)
    if db_snippet is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return db_snippet

@router.put("/{snippet_id}", response_model=Snippet)
def update_snippet(
    snippet_id: int, 
    snippet: SnippetUpdate, 
    db: Session = Depends(get_db)
):
    db_snippet = crud_snippet.update_snippet(db, snippet_id, snippet)
    if db_snippet is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return db_snippet