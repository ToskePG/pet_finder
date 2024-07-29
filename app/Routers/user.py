from ..database import models
from ..schemas import schemas
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from ..database.db import get_db
from sqlalchemy.orm import Session
from ..security import auth
from ..database import crud
from datetime import timedelta
from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post('/register/', response_model=schemas.User)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logging.info("Starting registration process")

    if not models.User.validate_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email address")
    
    hashed_password = auth.get_password_hash(password=user.password)
    user_data = user.dict(exclude={"password"})
    db_user = models.User(**user_data, password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logging.info(f"User registered successfully: {db_user.username}")
    return db_user

@router.post('/token', response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_username_for_token(db, form_data.username)
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

#Here im trying to verify the currently logged in user using JWT token
@router.get('/me', response_model=schemas.User)
async def get_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

#List all users, its more for testing the registration endpoint, but maybe it will still be needed
@router.get('/all_users', response_model=list[schemas.User])
async def read_users(skip: int=0, limit: int=0, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users