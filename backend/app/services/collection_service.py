from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.collection import Collection
from app.schemas.collection import CollectionCreate, CollectionUpdate

def get_collection_or_404(db: Session, collection_id: int, user_id: int) -> Collection:
    collection = db.query(Collection).filter(Collection.id == collection_id, Collection.user_id == user_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

def create_collection(db: Session, obj_in: CollectionCreate, user_id: int) -> Collection:
    db_obj = Collection(**obj_in.model_dump(), user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_collection(db: Session, collection_id: int, obj_in: CollectionUpdate, user_id: int) -> Collection:
    db_obj = get_collection_or_404(db, collection_id, user_id)
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_collection(db: Session, collection_id: int, user_id: int):
    db_obj = get_collection_or_404(db, collection_id, user_id)
    db.delete(db_obj)
    db.commit()