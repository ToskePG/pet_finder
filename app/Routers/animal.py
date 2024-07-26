from ..database import models
from ..schemas import schemas
from ..database.db import get_db
from sqlalchemy.orm import Session
from ..security import auth
from ..database import crud
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post('/animals', response_model=schemas.Animal)
async def create_animal(animal: schemas.AnimalCreate, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    animal_dict = animal.model_dump()
    db_animal = models.Animal(**animal_dict, user_id = current_user.user_id)
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

@router.get('/animals/id/{animal_id}', response_model = schemas.Animal)
async def read_animal(animal_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    db_animal = crud.get_animal(db=db, animal_id=animal_id)
    if not db_animal:
        raise HTTPException(status_code=404, detail="This animal does not exist")
    return db_animal

@router.get('/animals', response_model= list[schemas.Animal])
async def read_all_animals(category: str = None, breed: str = None,
                           age: int = None, coatLength: str = None, color: str = None,
                           gender: str = None, size: str = None, name: str = None, id: int = None,
                            current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    
    db_animals = crud.get_animals(animal_type=category, animal_breed=breed,
                                animal_age = age, animal_coat_length = coatLength,
                                animal_color = color, animal_gender = gender,
                                animal_size = size, animal_name = name, animal_id = id, db=db)
    return db_animals



#@router.delete('/animals/{animal_id}', status_code=status.HTTP_204_NO_CONTENT)
#def delete_animal(animal_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):

