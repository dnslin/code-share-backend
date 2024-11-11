from pydantic import BaseModel
from datetime import datetime
from typing import Optional  # 导入 Optional

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None  # 使用 Optional 替代 |

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True