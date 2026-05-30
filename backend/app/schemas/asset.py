from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.tag import TagResponse

class AssetResponse(BaseModel):
    id: int
    title: str
    file_url: str
    collection_id: int
    created_at: datetime
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True