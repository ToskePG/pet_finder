from ..database import models
from ..schemas import schemas
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from ..database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ..security import auth
from ..database import crud
from datetime import timedelta
from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.email_utils import send_email
from ..utils.token_utils import create_confirmation_token
import logging
import jwt
from ..security.auth import SECRET_KEY, ALGORITHM

router = APIRouter()

@router.post('/register/', response_model=schemas.UserResponse, tags=["User"])
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    if not models.User.validate_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email address")
    
    db_user_by_email = await crud.get_user_by_email(db=db, email=user.email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user_by_username = await crud.get_user_by_username(db=db, username=user.username)
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = auth.get_password_hash(password=user.password)
    user_data = user.dict(exclude={"password"})
    db_user = models.User(**user_data, password=hashed_password, is_confirmed=False)  # Set is_confirmed to False
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate email confirmation token
    token = auth.create_confirmation_token(email=user.email)
    confirmation_link = f"http://localhost:8000/confirm-email/?token={token}"
    email_body = f"Please confirm your email by clicking the following link: {confirmation_link}"
    
    send_email(to_email=user.email, subject="Email Confirmation", body=email_body)
    
    return db_user

@router.get('/confirm-email/', tags=["User"])
async def confirm_email(token: str, db: AsyncSession = Depends(get_db)):
    try:
        # Decode the token to get the email address
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    # Retrieve the user by email
    db_user = await crud.get_user_by_email(db=db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the user is already confirmed
    if db_user.is_confirmed:
        return {"message": "Email already confirmed"}
    
    # Update the user to set is_confirmed to True
    db_user.is_confirmed = True
    db.commit()
    db.refresh(db_user)
    
    return {"message": "Email confirmed successfully"}

@router.patch('/{user_id}/admin', response_model=schemas.UserResponse, tags=["User"])
async def assign_admin_role(user_id: int, current_user: schemas.User = Depends(auth.get_current_admin_user), db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_id(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.is_admin = True
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post('/token', response_model=schemas.Token, tags=["User"])
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
@router.get('/me', response_model=schemas.User, tags=["User"])
async def get_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user


@router.get('/{user_id}', response_model=schemas.UserResponse, tags=["User"])
async def read_user_by_id(user_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_id(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get('/{email}', response_model=schemas.UserResponse, tags=["User"])
async def read_user_by_email(user_email: str, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(email=user_email, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@router.get('/{username}', response_model=schemas.UserResponse, tags=["User"])
async def read_user_by_username(username: str, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_username(username=username, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
    

#List all users, its more for testing the registration endpoint, but maybe it will still be needed
@router.get('/', response_model=list[schemas.User], tags=["User"])
async def read_users(skip: int=0, limit: int=0, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db=db, skip=skip, limit=limit)
    return users


@router.patch('/{user_id}', response_model = schemas.UserResponse, tags=["User"])
async def update_user(user_id: int, user_update: schemas.UserUpdate, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    if user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to change this user")
    db_user = await crud.patch_user(user_id=user_id, user_update=user_update, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')
    if db_user=="Already exists":
        raise HTTPException(status_code=400, detail="Username already exists")
    return db_user


@router.delete('/{user_id}/', status_code=status.HTTP_204_NO_CONTENT, tags=["User"])
async def delete_user(user_id: int, current_user: schemas.User = Depends(auth.get_current_admin_user), db: AsyncSession = Depends(get_db)):
    db_user = await crud.delete_user(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return