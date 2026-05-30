from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagResponse
from app.services.tag_service import get_tag_or_404, create_tag
from app.services.asset_service import get_asset_or_404

router = APIRouter()

@router.post("/", response_model=TagResponse, status_code=201)
def create_new_tag(
    tag_in: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_tag(db, tag_in)

@router.get("/", response_model=List[TagResponse])
def get_all_tags(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Tag).all()

@router.post("/{asset_id}/assign", status_code=200)
def assign_tag_to_asset(
    asset_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    asset = get_asset_or_404(db, asset_id, current_user.id)
    tag = get_tag_or_404(db, tag_id)
    
    if tag not in asset.tags:
        asset.tags.append(tag)
        db.commit()
    
    return {"message": "Tag assigned successfully"}

@router.delete("/{id}", status_code=204)
def delete_tag(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Tags are global in this design, so handle deletion carefully
    tag = get_tag_or_404(db, id)
    db.delete(tag)
    db.commit()