from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .. import crud, schemas
from ..security import auth

router = APIRouter()

# Create a new post
@router.post("/posts", response_model=schemas.Post)
async def create_post(post: schemas.CreatePost, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_post = await crud.create_post(db, post, user_id=current_user.user_id)
    return db_post

# Get a post by ID
@router.get("/posts/id/{post_id}", response_model=schemas.Post)
async def get_post(post_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_post = await crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

# Get all posts with optional pagination
@router.get("/posts", response_model=list[schemas.Post])
async def get_posts(skip: int = 0, limit: int = 10, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.get_posts(db, skip=skip, limit=limit)

# Update a post
@router.put("/posts/{post_id}", response_model=schemas.Post)
async def update_post(post_id: int, post: schemas.CreatePost, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_post = await crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this post")
    db_post = await crud.update_post(db, post_id, post)
    return db_post

# Delete a post
@router.delete("/posts/{post_id}", response_model=schemas.Post)
async def delete_post(post_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_post = await crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this post")
    await crud.delete_post(db, post_id)
    return db_post
