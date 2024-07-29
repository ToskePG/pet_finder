from ..schemas import schemas
from ..database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from ..security import auth
from ..database import crud
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post("/", response_model=schemas.LocationResponse)
async def create_location(location: schemas.LocationCreate, current_user:schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_location = await crud.create_location(location = location, db=db)
    return db_location

@router.get('/{location_id}', response_model=schemas.LocationResponse)
async def read_location(location_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_location = await crud.get_location(location_id=location_id, db=db)
    if not db_location:
        raise HTTPException(status_code=404, detail="This location does not exist")
    return db_location

@router.get('/', response_model=list[schemas.LocationResponse])
async def read_locations(skip: int = 0, limit: int = 0, current_user: schemas.User = Depends(auth.get_current_user),db: AsyncSession = Depends(get_db)):
    db_locations = await crud.get_locations(skip=skip, limit=limit, db=db)
    return db_locations

@router.delete('/{location_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(location_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_location = await crud.delete_location(location_id= location_id, db=db)
    if not db_location:
        raise HTTPException(status_code=404, detail="This location does not exist")
    return 

