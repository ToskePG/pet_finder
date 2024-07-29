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

#AnimalType

@router.post("/animal_types", response_model = schemas.AnimaTypeResponse)
async def create_animal_type(animal_type: schemas.AnimalTypeCreate, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_animal_type = await crud.create_animal_type(db, animal_type)
    return db_animal_type

@router.get("/animal_types/{animal_type_id}", response_model = schemas.AnimaTypeResponse)
async def get_animal_type(animal_type_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_animal_type = await crud.get_animal_type(db, animal_type_id)
    if not db_animal_type:
        raise HTTPException(status_code=404, detail="Animal type not found")
    return db_animal_type

@router.get("/animal_types", response_model=list[schemas.AnimaTypeResponse])
async def get_animal_types(skip: int = 0, limit: int = 0, db: AsyncSession = Depends(get_db)):
    db_animal_types = await crud.get_animal_types(db=db, skip=skip, limit=limit)
    return db_animal_types

@router.delete("/animal_type/{animal_type_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_animal_type(animal_type_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):

    db_animal_type = await crud.delete_animal_type(animal_type_id = animal_type_id, db=db)
    if not db_animal_type:
        raise HTTPException(status_code=404, detail="Animal type not found")
    return

#Animal
@router.post('/', response_model=schemas.Animal)
async def create_animal(animal: schemas.AnimalCreate, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_animal_type = await crud.get_animal_type(db=db, animal_type_id=animal.animal_type_id)
    if not db_animal_type:
        raise HTTPException(status_code=404, detail="This animal typed does not exist")
    db_animal = await crud.create_animal(animal=animal, user_id = current_user.user_id, db=db)
    return db_animal

@router.get('/{animal_id}', response_model = schemas.Animal)
async def read_animal(animal_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_animal = await crud.get_animal(db=db, animal_id=animal_id)
    if not db_animal:
        raise HTTPException(status_code=404, detail="This animal does not exist")
    return db_animal

@router.get('/users/{user_id}', response_model=list[schemas.Animal])
async def read_animals_by_user_id(user_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="This user does not exist")
    db_animals = await crud.get_animals_by_user_id(db=db, user_id = user_id)
    
    return db_animals

@router.get('/', response_model= list[schemas.Animal])
async def read_animals(skip: int = 0, limit: int = 0, category: str = None, breed: str = None,
                           age: int = None, coatLength: str = None, color: str = None,
                           gender: str = None, size: str = None, name: str = None, id: int = None,
                           user_id: int = None, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    
    db_animals = await crud.get_animals(skip=skip, limit=limit, animal_type=category, animal_breed=breed,
                                animal_age = age, animal_coat_length = coatLength,
                                animal_color = color, animal_gender = gender,
                                animal_size = size, animal_name = name, animal_id = id,
                                user_id = user_id, db=db)
    
    return db_animals

@router.patch('/{animal_id}', response_model=schemas.AnimalResponse)
async def update_animal(animal_update: schemas.AnimalUpdate, animal_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_animal = await crud.get_animal(animal_id=animal_id, db=db)
    
    if db_animal.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this animal")
    
    if animal_update.animal_type_id is not None:
        db_animal_type = await crud.get_animal_type(animal_type_id=animal_update.animal_type_id, db=db)
        if not db_animal_type:
            raise HTTPException(status_code=404, detail="Animal type not found")
        
    if animal_update.location is not None:
        db_location = await crud.get_location(location_id=animal_update.location, db=db)
        if not db_location:  
            raise HTTPException(status_code=404, detail="Location not found")
        

    db_animal = await crud.patch_animal(animal_id=animal_id, animal_update=animal_update, db=db)
    return db_animal
    
    

@router.delete('/{animal_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_animal(animal_id: int,  current_user: schemas.User = Depends(auth.get_current_user), db: AsyncSession = Depends(get_db)):
    db_animal = await crud.delete_animal(animal_id=animal_id, db=db, user_id = current_user.user_id)
    if db_animal == "Not authorized":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this animal")
    if not db_animal:
        raise HTTPException(status_code=404, detail="Animal does not exist")
    return