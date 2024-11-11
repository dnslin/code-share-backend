from fastapi import APIRouter
from app.core.languages_config import LANGUAGES_CONFIG
import logging

# 设置日志级别
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 在模块级别打印，确认导入是否成功
print("Imported LANGUAGES_CONFIG:", LANGUAGES_CONFIG)

router = APIRouter()

@router.get("/languages")
async def get_supported_languages():
    logger.info("Accessing languages endpoint")
    languages_data = dict(LANGUAGES_CONFIG)
    logger.info(f"Languages data: {languages_data}")
    
    return {
        "success": True,
        "data": languages_data
    }