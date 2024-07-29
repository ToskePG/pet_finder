from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.db import get_db
from ..database import crud
from ..schemas import schemas
from ..security import auth
from datetime import datetime

router = APIRouter()

#Post Endpoints
@router.post("/create_post", response_model=schemas.PostResponse)
async def create_post(post: schemas.CreatePost, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_post = await crud.create_post(db, post)
    return db_post

@router.get("/{post_id}", response_model=schemas.PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    db_post = await crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.get("/", response_model=list[schemas.PostResponse])
async def get_posts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    db_posts = await crud.get_posts(db,skip,limit)
    return db_posts

@router.put("/{post_id}", response_model=schemas.PostResponse)
async def update_post(post_id: int, post: schemas.CreatePost, db: AsyncSession = Depends(get_db)):
    db_post = crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post = crud.update_post(db, post_id, post)
    return db_post

@router.delete("/{post_id}", response_model=schemas.PostResponse)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    db_post = crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    crud.delete_post(db, post_id)
    return db_post

# List all posts by the current user
@router.get("/user", response_model=list[schemas.PostResponse])
async def get_posts_by_user(
    skip: int = 0,
    limit: int = 10,
    current_user: schemas.User = Depends(auth.get_current_user),  # Ensure user is authenticated
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user.user_id
    posts = crud.get_posts_by_user(db, user_id, skip, limit)
    return posts

# List all posts by a specific username
@router.get("/{username}", response_model=list[schemas.PostResponse])
async def get_posts_by_username(
    username: str,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    posts = crud.get_posts_by_username(db, username, skip, limit)
    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found for the given username")
    return posts

# Endpoint to filter posts by user_id
@router.get("/by_user_id", response_model=list[schemas.PostResponse])
async def get_posts_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    posts = crud.get_posts_by_user_id(db, user_id)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for the given user ID")
    return posts

# Endpoint to filter posts by email
@router.get("/by_email", response_model=list[schemas.PostResponse])
async def get_posts_by_email(email: str, db: AsyncSession = Depends(get_db)):
    posts = crud.get_posts_by_email(db, email)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for the given email")
    return posts

# List all posts by a specific username where the current user has requests
@router.get("/user/{username}", response_model=list[schemas.PostResponse])
async def get_posts_by_username(
    username: str,
    skip: int = 0,
    limit: int = 10,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    posts = crud.get_posts_by_username(db, username, current_user.user_id, skip, limit)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for the given username with your requests")
    return posts

# Endpoint to filter posts by email where the current user has requests
@router.get("/by_email_requests", response_model=list[schemas.PostResponse])
async def get_posts_by_email(
    email: str,
    skip: int = 0,
    limit: int = 10,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    posts = crud.get_posts_by_email(db, email, current_user.user_id, skip, limit)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found for the given email with your requests")
    return posts

# List all posts by the current user where the specified username has made requests
@router.get("/current_user_with_requests/{username}", response_model=list[schemas.PostResponse])
async def get_posts_by_user_with_requests(
    username: str,
    skip: int = 0,
    limit: int = 10,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    posts = crud.get_posts_by_user_with_requests(db, username, current_user.user_id, skip, limit)
    if not posts:
        raise HTTPException(status_code=404, detail="No posts found where the specified user has made requests")
    return posts