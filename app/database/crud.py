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

def get_animals(animal_type: Optional[str], animal_breed: Optional[str],
                animal_age: Optional[int], animal_coat_length: Optional[str],
                animal_color: Optional[str], animal_gender: Optional[str], animal_size: Optional[str],
                animal_name: Optional[str], animal_id: Optional[int], db: Session):
    
    query = db.query(models.Animal)

    if animal_type:
        query = query.filter(models.Animal.animal_type == animal_type)
    if animal_breed:
        query = query.filter(models.Animal.animal_breed == animal_breed)
    if animal_age is not None:
        query = query.filter(models.Animal.animal_age == animal_age)
    if animal_coat_length:
        query = query.filter(models.Animal.animal_coatLength == animal_coat_length)
    if animal_color:
        query = query.filter(models.Animal.animal_color == animal_color)
    if animal_gender:
        query = query.filter(models.Animal.animal_gender == animal_gender)
    if animal_size:
        query = query.filter(models.Animal.animal_size == animal_size)
    if animal_name:
        query = query.filter(models.Animal.animal_name == animal_name)
    if animal_id is not None:
        query = query.filter(models.Animal.animal_id == animal_id)

    return query.all()


def delete_animal(db: Session, animal_id: int):
    db_animal = get_animal(db=db, animal_id=animal_id)
    if not db_animal:
        return None
    db.delete(db_animal)
    db.commit()
    return db_animal
    