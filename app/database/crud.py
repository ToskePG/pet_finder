from ..database.db import get_db
from sqlalchemy.orm import Session
from ..database import models
from ..schemas import schemas
from typing import Optional
from sqlalchemy import and_

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

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import update, delete
from ..database import models
from ..schemas import schemas

# Create a new post
async def create_post(db: AsyncSession, post: schemas.CreatePost) -> models.Post:
    db_post = models.Post(**post.dict())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

# Get a post by ID
async def get_post(db: AsyncSession, post_id: int) -> models.Post:
    result = await db.execute(select(models.Post).where(models.Post.post_id == post_id))
    return result.scalar_one_or_none()

# Get all posts with optional pagination
async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[models.Post]:
    result = await db.execute(select(models.Post).offset(skip).limit(limit))
    return result.scalars().all()

#Update a post
async def update_post(db: AsyncSession, post_id: int, post: schemas.CreatePost) -> Optional[models.Post]:
    result = await db.execute(select(models.Post).where(models.Post.post_id == post_id))
    db_post = result.scalar_one_or_none()
    if db_post is None:
        return None
    for key, value in post.dict().items():
        setattr(db_post, key, value)
    await db.commit()
    await db.refresh(db_post)
    return db_post

#Delete a post 
async def delete_post(db: AsyncSession, post_id: int) -> Optional[models.Post]:
    result = await db.execute(select(models.Post).where(models.Post.post_id == post_id))
    db_post = result.scalar_one_or_none()
    if db_post is None:
        return None
    await db.delete(db_post)
    await db.commit()
    return db_post
