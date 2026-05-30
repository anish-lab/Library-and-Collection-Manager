from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.tag import Tag
from app.schemas.tag import TagCreate

def get_tag_or_404(db: Session, tag_id: int) -> Tag:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

def create_tag(db: Session, obj_in: TagCreate) -> Tag:
    existing = db.query(Tag).filter(Tag.name == obj_in.name.lower()).first()
    if existing:
        return existing
    
    db_tag = Tag(name=obj_in.name.lower())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag