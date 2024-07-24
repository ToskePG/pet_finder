from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.db import get_db
from ..database import crud
from ..schemas import schemas
from ..security import auth

router = APIRouter()

# PostType Endpoints

@router.post("/post_types", response_model=schemas.PostTypeResponse)
async def create_post_type(post_type: schemas.PostTypeCreate, db: AsyncSession = Depends(get_db)):
    db_post_type = await crud.create_post_type(db, post_type)
    return db_post_type

@router.get("/post_types/{post_type_id}", response_model=schemas.PostTypeResponse)
async def get_post_type(post_type_id: int, db: AsyncSession = Depends(get_db)):
    db_post_type = await crud.get_post_type(db, post_type_id)
    if not db_post_type:
        raise HTTPException(status_code=404, detail="Post type not found")
    return db_post_type

@router.get("/post_types", response_model=list[schemas.PostTypeResponse])
async def get_post_types(db: AsyncSession = Depends(get_db)):
    return await crud.get_post_types(db)

# Existing Post Endpoints

@router.post("/posts", response_model=schemas.PostResponse)
async def create_post(post: schemas.CreatePost, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_post = await crud.create_post(db, post)
    return db_post

@router.get("/posts/{post_id}", response_model=schemas.PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    db_post = await crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.get("/posts", response_model=list[schemas.PostResponse])
async def get_posts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_posts(db, skip=skip, limit=limit)

@router.put("/posts/{post_id}", response_model=schemas.PostResponse)
async def update_post(post_id: int, post: schemas.CreatePost, db: AsyncSession = Depends(get_db)):
    db_post = await crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post = await crud.update_post(db, post_id, post)
    return db_post

@router.delete("/posts/{post_id}", response_model=schemas.PostResponse)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    db_post = await crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    await crud.delete_post(db, post_id)
    return db_post

# List all posts by the current user
@router.get("/posts/user", response_model=List[schemas.PostResponse])
async def get_posts_by_user(
    skip: int = 0,
    limit: int = 10,
    current_user: schemas.User = Depends(auth.get_current_user),  # Ensure user is authenticated
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user.user_id
    posts = await crud.get_posts_by_user(db, user_id, skip, limit)
    return posts

# List all posts by a specific username
@router.get("/posts/user/{username}", response_model=List[schemas.PostResponse])
async def get_posts_by_username(
    username: str,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    posts = await crud.get_posts_by_username(db, username, skip, limit)
    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found for the given username")
    return posts