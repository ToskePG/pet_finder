from ..database import models
from ..schemas import schemas
from ..database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from ..security import auth
from ..database import crud
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

#PetType

@router.post("/pet_types", response_model = schemas.PetTypeResponse, tags=["Pet Type"])
async def create_pet_type(pet_type: schemas.PetTypeCreate, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_pet_type = await crud.create_pet_type(db, pet_type)
    return db_pet_type

@router.get("/pet_types/{pet_type_id}", response_model = schemas.PetTypeResponse, tags=["Pet Type"])
async def get_pet_type(pet_type_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_pet_type = await crud.get_pet_type(db, pet_type_id)
    if not db_pet_type:
        raise HTTPException(status_code=404, detail="Pet type not found")
    return db_pet_type

@router.get("/pet_types", response_model=list[schemas.PetTypeResponse], tags=["Pet Type"])
async def get_pet_types(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    db_pet_types = await crud.get_pet_types(db=db, skip=skip, limit=limit)
    return db_pet_types

@router.delete("/pet_type/{pet_type_id}", status_code= status.HTTP_204_NO_CONTENT, tags=["Pet Type"])
async def delete_pet_type(pet_type_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):

    db_pet_type = await crud.delete_pet_type(pet_type_id = pet_type_id, db=db)
    if not db_pet_type:
        raise HTTPException(status_code=404, detail="Pet type not found")
    return

#Animal
@router.post('/', response_model=schemas.PetResponse, tags=["Pet"])
async def create_pet(pet: schemas.PetCreate, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_pet_type = await crud.get_pet_type(db=db, pet_type_id=pet.pet_type_id)
    if not db_pet_type:
        raise HTTPException(status_code=404, detail="This pet type does not exist")
    
    db_pet_location = await crud.get_location(db=db, location_id = pet.location)
    if not db_pet_location:
        raise HTTPException(status_code=404, detail="This city does not exist")
    
    db_pet = await crud.create_pet(pet=pet, user_id = current_user.user_id, db=db)
    return db_pet

@router.get('/{pet_id}', response_model = schemas.PetResponse, tags=["Pet"])
async def read_pet(pet_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_pet = await crud.get_pet(db=db, pet_id=pet_id)
    if not db_pet:
        raise HTTPException(status_code=404, detail="This pet does not exist")
    return db_pet

@router.get('/users/{user_id}', response_model=list[schemas.PetResponse], tags=["Pet"])
async def read_pets_by_user_id(user_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="This user does not exist")
    db_pets = await crud.get_pets_by_user_id(db=db, user_id = user_id)
    
    return db_pets

@router.get('/', response_model= list[schemas.PetResponse], tags=["Pet"])
async def read_pets(skip: int = 0, limit: int = 10, category: str = None, breed: str = None,
                           age: int = None, coatLength: str = None, color: str = None,
                           gender: str = None, size: str = None, name: str = None, id: int = None,
                           user_id: int = None, location: str = None, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    
    db_pets = await crud.get_pets(skip=skip, limit=limit, pet_type=category, pet_breed=breed,
                                pet_age = age, pet_coat_length = coatLength,
                                pet_color = color, pet_gender = gender,
                                pet_size = size, pet_name = name, pet_id = id, pet_location = location,
                                user_id = user_id, db=db)
    
    return db_pets

@router.patch('/{pet_id}', response_model=schemas.PetResponse, tags=["Pet"])
async def update_pet(pet_update: schemas.PetUpdate, pet_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_pet = await crud.get_pet(pet_id=pet_id, db=db)
    
    if db_pet.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this pet")
    
    if pet_update.pet_type_id is not None:
        db_pet_type = await crud.get_pet_type(pet_type_id=pet_update.pet_type_id, db=db)
        if not db_pet_type:
            raise HTTPException(status_code=404, detail="Pet type not found")
        
    if pet_update.location is not None:
        db_location = await crud.get_location(location_id=pet_update.location, db=db)
        if not db_location:  
            raise HTTPException(status_code=404, detail="Location not found")
        

    db_pet = await crud.patch_pet(pet_id=pet_id, pet_update=pet_update, db=db)
    return db_pet
    
    

@router.delete('/{pet_id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Pet"])
async def delete_pet(pet_id: int,  current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_pet = await crud.delete_pet(pet_id=pet_id, db=db, user_id = current_user.user_id)
    if db_pet == "Not authorized":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this pet")
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet does not exist")
    return