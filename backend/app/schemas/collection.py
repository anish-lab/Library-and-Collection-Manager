from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.asset import AssetResponse

class CollectionCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CollectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CollectionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CollectionDetailResponse(CollectionResponse):
    assets: List[AssetResponse] = []