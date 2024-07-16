from .. import models
from .. import schemas

from fastapi import APIRouter, Depends, HTTPException
from ..db import get_db
from sqlalchemy.orm import Session
from .. import auth
from .. import crud


router = APIRouter()

@router.post('/register/', response_model=schemas.User)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not models.User.validate_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email address")
    
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail = "Email already registered")
    db_user = crud.get_user_by_username(db=db, username = user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = auth.get_password_hash(password=user.password)
    user_dict = user.model_dump()
    user_dict.pop("password")
    db_user = models.User(**user_dict, password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user