from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.collection import Collection
from app.schemas.collection import CollectionCreate, CollectionUpdate, CollectionResponse, CollectionDetailResponse
from app.services.collection_service import create_collection, update_collection, delete_collection, get_collection_or_404

router = APIRouter()

@router.post("/", response_model=CollectionResponse, status_code=201)
def create(
    collection_in: CollectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_collection(db, collection_in, current_user.id)

@router.get("/", response_model=List[CollectionResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Collection).filter(Collection.user_id == current_user.id).all()

@router.get("/{id}", response_model=CollectionDetailResponse)
def get_one(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_collection_or_404(db, id, current_user.id)

@router.put("/{id}", response_model=CollectionResponse)
def update(
    id: int,
    collection_in: CollectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_collection(db, id, collection_in, current_user.id)

@router.delete("/{id}", status_code=204)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    delete_collection(db, id, current_user.id)