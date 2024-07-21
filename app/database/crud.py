from ..database.db import get_db
from sqlalchemy.orm import Session
from ..database import models
from ..schemas import schemas
from typing import Optional
from sqlalchemy import and_
from ..database.models import Post
from ..schemas.schemas import CreatePost, PostBase

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user


#Animals

def create_animal(db: Session, animal: schemas.AnimalCreate):

    db_animal = models.Animal(**animal.model_dump())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

def get_animal(db: Session, animal_id: int):
    return db.query(models.Animal).filter(models.Animal.animal_id == animal_id).first()

def get_animals(animal_type: Optional[str], animal_breed: Optional[str], db: Session):
    if animal_type and animal_breed:
        return db.query(models.Animal).filter(and_(models.Animal.animal_type == animal_type, models.Animal.animal_breed == animal_breed)).all()
    if animal_type:
        return db.query(models.Animal).filter(models.Animal.animal_type == animal_type).all()
    
    return db.query(models.Animal)

# Create a new post
async def create_post(db: Session, post: CreatePost) -> Post:
    db_post = Post(**post.dict())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post