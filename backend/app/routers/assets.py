from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.asset import Asset
from app.models.collection import Collection
from app.models.tag import Tag
from app.models.asset import asset_tags
from app.schemas.asset import AssetResponse
from app.services.asset_service import save_upload_file, delete_file, get_asset_or_404, create_asset

router = APIRouter()

@router.post("/", response_model=AssetResponse, status_code=201)
def upload_asset(
    title: str = Form(...),
    collection_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify collection ownership
    collection = db.query(Collection).filter(Collection.id == collection_id, Collection.user_id == current_user.id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found or access denied")
    
    file_url = save_upload_file(file)
    return create_asset(db, title=title, collection_id=collection_id, file_url=file_url)

@router.get("/", response_model=List[AssetResponse])
def get_assets(
    tag: Optional[str] = None,
    collection: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Asset).join(Collection).filter(Collection.user_id == current_user.id)
    
    if collection:
        query = query.filter(Asset.collection_id == collection)
    if search:
        query = query.filter(Asset.title.ilike(f"%{search}%"))
    if tag:
        query = query.join(asset_tags).join(Tag).filter(Tag.name.ilike(f"%{tag}%"))
        
    return query.all()

@router.get("/{id}", response_model=AssetResponse)
def get_asset(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_asset_or_404(db, id, current_user.id)

@router.put("/{id}", response_model=AssetResponse)
def update_asset_info(
    id: int,
    title: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Note: Using form data for simple update to match POST pattern, but JSON could be used
    asset = get_asset_or_404(db, id, current_user.id)
    asset.title = title
    db.commit()
    db.refresh(asset)
    return asset

@router.delete("/{id}", status_code=204)
def delete_asset(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    asset = get_asset_or_404(db, id, current_user.id)
    delete_file(asset.file_url)
    db.delete(asset)
    db.commit()