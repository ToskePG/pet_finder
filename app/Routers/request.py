from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database.db import get_db
from ..database import crud
from ..schemas import schemas
from ..security import auth  # Adjust the import based on your directory structure

router = APIRouter()

# Create a new request
@router.post("/requests", response_model=schemas.RequestResponse)
async def create_request(
    request: schemas.RequestCreate,
    current_user: schemas.User = Depends(auth.get_current_user),  # Ensure user is authenticated
    db: AsyncSession = Depends(get_db)
):
    db_request = await crud.create_request(db, request)
    return db_request

# Get a request by ID
@router.get("/requests/{request_id}", response_model=schemas.RequestResponse)
async def get_request(
    request_id: int,
    current_user: schemas.User = Depends(auth.get_current_user),  # Ensure user is authenticated
    db: AsyncSession = Depends(get_db)
):
    db_request = await crud.get_requests(db, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

# Get all requests with optional pagination
@router.get("/requests", response_model=List[schemas.RequestResponse])
async def get_requests(
    skip: int = 0,
    limit: int = 10,
    current_user: schemas.User = Depends(auth.get_current_user),  # Ensure user is authenticated
    db: AsyncSession = Depends(get_db)
):
    requests = await crud.get_requests(db, skip, limit)
    return requests

# Update a request
@router.put("/requests/{request_id}", response_model=schemas.RequestResponse)
async def update_request(
    request_id: int,
    request: schemas.RequestCreate,
    current_user: schemas.User = Depends(auth.get_current_user),  # Ensure user is authenticated
    db: AsyncSession = Depends(get_db)
):
    db_request = await crud.update_request(db, request_id, request)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

# Delete a request
@router.delete("/requests/{request_id}", response_model=schemas.RequestResponse)
async def delete_request(
    request_id: int,
    current_user: schemas.User = Depends(auth.get_current_user),  # Ensure user is authenticated
    db: AsyncSession = Depends(get_db)
):
    db_request = await crud.delete_request(db, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

# List all requests by the current user
@router.get("/requests/user", response_model=List[schemas.RequestResponse])
async def get_requests_by_user(
    skip: int = 0,
    limit: int = 10,
    current_user: schemas.User = Depends(auth.get_current_user),  # Ensure user is authenticated
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user.user_id
    requests = await crud.get_requests_by_user(db, user_id, skip, limit)
    return requests