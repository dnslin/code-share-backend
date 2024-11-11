from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.core.languages_config import LANGUAGES_CONFIG
from app.database import get_db
from app.models.snippet import Snippet
import logging
import shortuuid
from datetime import datetime

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