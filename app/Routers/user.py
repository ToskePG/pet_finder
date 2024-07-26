from ..database import models
from ..schemas import schemas
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from ..database.db import get_db
from sqlalchemy.orm import Session
from ..security import auth
from ..database import crud
from datetime import timedelta


router = APIRouter()

@router.post('/register/', response_model=schemas.User)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Validate email
    if not models.User.validate_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email address")
    
    # Check if email is already registered
    db_user_by_email = crud.get_user_by_email(db=db, email=user.email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username is already registered
    db_user_by_username = crud.get_user_by_username(db=db, username=user.username)
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash the user's password
    hashed_password = auth.get_password_hash(password=user.password)
    
    # Prepare user data for saving, excluding the plain password
    user_data = user.dict(exclude={"password"})
    db_user = models.User(**user_data, password=hashed_password)
    
    # Save the new user to the database
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

#Here im trying to verify the currently logged in user using JWT token
@router.get('/me', response_model=schemas.User)
async def get_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

#List all users, its more for testing the registration endpoint, but maybe it will still be needed
@router.get('/users/', response_model=list[schemas.User])
async def read_users(skip: int=0, limit: int=0, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@router.delete('/users/{user_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user: schemas.User = Depends(auth.get_current_admin_user), db: Session = Depends(get_db)):
    
    db_user = crud.delete_user(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return 

