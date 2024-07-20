from app.database import models
from app.schemas import schemas
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from app.database.db import get_db
from sqlalchemy.orm import Session
from app.security import auth
from app.database import crud


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

@router.post('/token', response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/users/', response_model=list[schemas.User])
async def read_users(skip: int=0, limit: int=0, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users