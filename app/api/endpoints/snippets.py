from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.core.languages_config import LANGUAGES_CONFIG
from app.database import get_db
from app.models.snippet import Snippet
import logging
import shortuuid
from datetime import datetime
from app.schemas.snippet import ShareCodeRequest, ShareCodeResponse, ShareLinkInfoResponse, ShareLinkContentResponse
from app.crud import crud_snippet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class SnippetCreate(BaseModel):
    code: str
    language: str
    title: Optional[str] = None
    serial: Optional[str] = None

@router.post("")
async def create_or_update_snippet(
    snippet: SnippetCreate,
    db: Session = Depends(get_db)
):
    try:
        if snippet.serial:
            existing_snippet = db.query(Snippet).filter(
                Snippet.sequence == snippet.serial
            ).first()
            
            if not existing_snippet:
                raise HTTPException(
                    status_code=404,
                    detail=f"Snippet with serial {snippet.serial} not found"
                )
            
            existing_snippet.code = snippet.code
            existing_snippet.language = snippet.language
            existing_snippet.title = snippet.title
            existing_snippet.updated_at = datetime.now()
            db.commit()
            
            return {
                "success": True,
                "data": existing_snippet.sequence
            }
        
        sequence = shortuuid.uuid()[:8]
        db_snippet = Snippet(
            sequence=sequence,
            code=snippet.code,
            language=snippet.language,
            title=snippet.title
        )
        
        db.add(db_snippet)
        db.commit()
        
        return {
            "success": True,
            "data": sequence
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        logger.error(f"Error processing snippet: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process snippet"
        )

@router.get("/languages")
async def get_supported_languages():
    logger.info("Accessing languages endpoint")
    languages_data = dict(LANGUAGES_CONFIG)
    return {
        "success": True,
        "data": languages_data
    }

@router.post("/share", response_model=ShareCodeResponse)
def share_code(
    share_request: ShareCodeRequest,
    db: Session = Depends(get_db)
):
    snippet, error = crud_snippet.create_share_link(db, share_request)
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # 构建分享信息
    share_info = {
        "shareLink": f"/share/{snippet.share_link}",
        "accessCode": snippet.access_code,
        "expireAt": snippet.expire_at.isoformat() if snippet.expire_at else "never",
        "createdAt": snippet.shared_at.isoformat()
    }
    
    return ShareCodeResponse(success=True, data=share_info)

@router.get("/share/{share_link}")
def get_shared_snippet(
    share_link: str,
    access_code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    snippet, error = crud_snippet.get_shared_snippet(db, share_link, access_code)
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    return {
        "success": True,
        "data": {
            "id": snippet.id,
            "code": snippet.code,
            "language": snippet.language,
            "createdAt": snippet.created_at.isoformat(),
            "expireAt": snippet.expire_at.isoformat() if snippet.expire_at else "never"
        }
    }

@router.get("/share/{share_link}/info", response_model=ShareLinkInfoResponse)
def get_share_info(
    share_link: str,
    db: Session = Depends(get_db)
):
    """获取分享链接的基本信息"""
    info, error = crud_snippet.get_share_link_info(db, share_link)
    
    if error:
        raise HTTPException(status_code=404, detail=error)
    
    return ShareLinkInfoResponse(success=True, data=info)

@router.post("/share/{share_link}/content", response_model=ShareLinkContentResponse)
def get_share_content(
    share_link: str,
    access_code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取分享内容"""
    snippet, error = crud_snippet.get_share_link_content(db, share_link, access_code)
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    return ShareLinkContentResponse(
        success=True,
        data={
            "code": snippet.code,
            "language": snippet.language,
            "title": getattr(snippet, 'title', None),
            "description": getattr(snippet, 'description', None),
            "createdAt": snippet.created_at,
            "expireAt": snippet.expire_at
        }
    )

@router.get("/share/{share_link}/raw")
def get_raw_code(
    share_link: str,
    access_code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取原始代码内容"""
    snippet, error = crud_snippet.get_share_link_content(db, share_link, access_code)
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    return Response(content=snippet.code, media_type="text/plain")