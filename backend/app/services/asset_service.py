import os
import uuid
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from app.models.asset import Asset
from app.models.collection import Collection
from app.models.tag import Tag
from app.models.asset import asset_tags

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "pdf"}

def get_asset_or_404(db: Session, asset_id: int, user_id: int) -> Asset:
    asset = db.query(Asset).join(Collection).filter(Asset.id == asset_id, Collection.user_id == user_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

def save_upload_file(upload_file: UploadFile) -> str:
    ext = upload_file.filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File extension not allowed: {ext}")
    
    filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join("uploads", filename)
    
    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())
    
    return f"/uploads/{filename}"

def delete_file(file_url: str):
    file_path = file_url.lstrip("/")
    if os.path.exists(file_path):
        os.remove(file_path)

def create_asset(db: Session, title: str, collection_id: int, file_url: str) -> Asset:
    db_asset = Asset(title=title, collection_id=collection_id, file_url=file_url)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset