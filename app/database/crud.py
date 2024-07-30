from ..database.db import get_db
from sqlalchemy.orm import Session
from ..database import models
from ..schemas import schemas
from typing import Optional
from sqlalchemy import and_
from ..security import auth



from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import update, delete
from ..database import models
from ..schemas import schemas


#GET users by ID
async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[schemas.User]: 
    result = db.execute(select(models.User).where(models.User.user_id == user_id))
    return result.scalar_one_or_none()


#GET users by EMAIL
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[schemas.User]:
    result = db.execute(select(models.User).where(models.User.email == email))
    return result.scalar_one_or_none()


#GET users by USERNAME
async def get_user_by_username(db: AsyncSession, username: str) -> Optional[schemas.User]:
    result = db.execute(select(models.User).where(models.User.username == username))
    user = result.scalar_one_or_none()
    return user


#GET all USERS
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[schemas.User]:
    result = db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

#PATCH user
async def patch_user(db: AsyncSession, user_id: int, user_update: schemas.UserUpdate) -> Optional[schemas.User]:
    if user_update.username:
        db_user = await get_user_by_username(db=db, username=user_update.username)
        if db_user:
            return "Already exists"
    
    db_user = await get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        return None
    
    for key, val in user_update.model_dump(exclude_unset = True).items():
        
        if key == "password":
            hashed_password = auth.get_password_hash(password=user_update.password)
            setattr(db_user, "password", hashed_password)
        else:
            setattr(db_user, key, val)
    db.commit()
    db.refresh(db_user)
    return db_user
    
    

#DELETE users by ID
async def delete_user(db: AsyncSession, user_id: int) -> Optional[schemas.User]:
    db_user = await get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user


#PetType

#CREATE PetType
async def create_pet_type(db: AsyncSession, pet_type: schemas.PetTypeCreate) -> schemas.PetType:
    db_pet_type = models.PetType(**pet_type.model_dump())
    db.add(db_pet_type)
    db.commit()
    db.refresh(db_pet_type)
    return db_pet_type

#GET PetType by ID
async def get_pet_type(db: AsyncSession, pet_type_id: int) -> Optional[schemas.PetType]:
    db_pet_type = db.execute(select(models.PetType).where(models.PetType.pet_type_id == pet_type_id))
    return db_pet_type.scalar_one_or_none()


#GET PetType
async def get_pet_types(db: AsyncSession, limit: int = 0, skip: int = 10) -> list[schemas.PetType]:
    db_pet_types = db.execute(select(models.PetType).offset(skip).limit(limit))
    return db_pet_types.scalars().all()

#Delete PetType by ID
async def delete_pet_type(pet_type_id: int, db: AsyncSession) -> Optional[schemas.PetType]:
    db_pet_type = db.execute(select(models.PetType).where(models.PetType.pet_type_id == pet_type_id))
    db_pet_type = db_pet_type.scalar_one_or_none()
    if not db_pet_type:
        return None
    db.delete(db_pet_type)
    db.commit()
    return db_pet_type




#CREATE Pet
async def create_pet(db: AsyncSession, user_id: int, pet: schemas.PetCreate) -> models.Pet:
    db_pet = models.Pet(**pet.model_dump(), user_id = user_id)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


#GET Pet by pet_ID
async def get_pet(db: AsyncSession, pet_id: int) -> Optional[schemas.Pet]:
    db_pet = db.execute(select(models.Pet).where(models.Pet.pet_id == pet_id))
    return db_pet.scalar_one_or_none()


#GET Pet by user_ID
async def get_pets_by_user_id(db: AsyncSession, user_id: int) -> Optional[list[schemas.Pet]]:
    db_pets = db.execute(select(models.Pet).where(models.Pet.user_id == user_id))
    return db_pets.scalars().all()


#FILTER pets
async def get_pets(pet_type: Optional[str], pet_breed: Optional[str],
                pet_age: Optional[int], pet_coat_length: Optional[str],
                pet_color: Optional[str], pet_gender: Optional[str], pet_size: Optional[str],
                pet_name: Optional[str], pet_id: Optional[int],
                 user_id: Optional[int], pet_location: Optional[str], db: AsyncSession, skip: int = 0, limit: int = 10) -> list[schemas.Pet]:
    
    query = select(models.Pet)

    if pet_type:
        query = query.join(models.PetType).where(models.PetType.pet_type == pet_type)
        
    if pet_breed:
        query = query.where(models.Pet.pet_breed == pet_breed)
    if pet_age is not None:
        query = query.where(models.Pet.pet_age == pet_age)
    if pet_coat_length:
        query = query.where(models.Pet.pet_coatLength == pet_coat_length)
    if pet_color:
        query = query.where(models.Pet.pet_color == pet_color)
    if pet_gender:
        query = query.where(models.Pet.pet_gender == pet_gender)
    if pet_size:
        query = query.where(models.Pet.pet_size == pet_size)
    if pet_name:
        query = query.where(models.Pet.pet_name == pet_name)
    if pet_id is not None:
        query = query.where(models.Pet.pet_id == pet_id)
    if user_id:
        query = query.where(models.Pet.user_id == user_id)
    
    if pet_location:
        query = query.join(models.Location).where(models.Location.city_name == pet_location)

    query = query.offset(skip).limit(limit)
    result = db.execute(query)
    return result.scalars().all()


async def patch_pet(pet_id: int, pet_update: schemas.PetUpdate, db: AsyncSession) -> schemas.Pet:
    db_pet = await get_pet(pet_id=pet_id, db=db)

    for key, val in pet_update.model_dump(exclude_unset = True).items():
         setattr(db_pet, key, val)
    db.commit()
    db.refresh(db_pet)
    return db_pet

#DELETE Pet by ID
async def delete_pet(db: AsyncSession, pet_id: int, user_id: int) -> Optional[schemas.Pet]:
    db_pet = await get_pet(db=db, pet_id=pet_id)
    if db_pet.user_id != user_id:
       return "Not authorized"
    if not db_pet:
        return None
    db.delete(db_pet)
    db.commit()
    return db_pet


    
#Location

#Create location
async def create_location(location: schemas.LocationCreate, db: AsyncSession) -> schemas.LocationResponse:
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


#GET a location by ID
async def get_location(location_id: int, db: AsyncSession):
    db_location = db.execute(select(models.Location).where(models.Location.location_id == location_id))
    return db_location.scalar_one_or_none()


#GET all locations
async def get_locations(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[schemas.Location]:
    db_locations = db.execute(select(models.Location).offset(skip).limit(limit))
    return db_locations.scalars().all()

#DELETE location by ID
async def delete_location(location_id: int, db: AsyncSession) -> Optional[schemas.Location]:
    db_location = await get_location(location_id=location_id, db=db)
    if not db_location:
        return None
    db.delete(db_location)
    db.commit()
    return db_location

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import update, delete
from ..database import models
from ..schemas import schemas

#PostType CRUD
async def create_post_type(db: AsyncSession, post_type: schemas.PostTypeCreate) -> models.PostType:
    db_post_type = models.PostType(**post_type.dict())
    db.add(db_post_type)
    await db.commit()
    await db.refresh(db_post_type)
    return db_post_type

async def get_post_type(db: AsyncSession, post_type_id: int) -> Optional[models.PostType]:
    result = await db.execute(select(models.PostType).where(models.PostType.post_type_id == post_type_id))
    return result.scalar_one_or_none()

async def get_post_types(db: AsyncSession) -> list[models.PostType]:
    result = await db.execute(select(models.PostType))
    return result.scalars().all()

# Create a new post
async def create_post(db: AsyncSession, post: schemas.CreatePost) -> models.Post:
    db_post = models.Post(**post.dict())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

# Get a post by ID
async def get_post(db: AsyncSession, post_id: int) -> models.Post:
    result = await db.execute(select(models.Post).where(models.Post.post_id == post_id))
    return result.scalar_one_or_none()

# Get all posts with optional pagination
async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[models.Post]:
    result = await db.execute(select(models.Post).offset(skip).limit(limit))
    return result.scalars().all()

#Update a post
async def update_post(db: AsyncSession, post_id: int, post: schemas.CreatePost) -> Optional[models.Post]:
    result = await db.execute(select(models.Post).where(models.Post.post_id == post_id))
    db_post = result.scalar_one_or_none()
    if db_post is None:
        return None
    for key, value in post.dict().items():
        setattr(db_post, key, value)
    await db.commit()
    await db.refresh(db_post)
    return db_post

#Delete a post 
async def delete_post(db: AsyncSession, post_id: int) -> Optional[models.Post]:
    result = await db.execute(select(models.Post).where(models.Post.post_id == post_id))
    db_post = result.scalar_one_or_none()
    if db_post is None:
        return None
    await db.delete(db_post)
    await db.commit()
    return db_post

async def get_posts_by_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10) -> list[models.Post]:
    result = await db.execute(
        select(models.Post)
        .where(models.Post.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_user_by_username_for_token(db: AsyncSession, username: str) -> Optional[models.User]:
    result = db.execute(select(models.User).where(models.User.username == username))
    user = result.scalar_one_or_none()
    return user

async def get_posts_by_username(db: AsyncSession, username: str, skip: int = 0, limit: int = 10) -> list[models.Post]:
    user = await get_user_by_username(db, username)
    if not user:
        return []  # User not found, return an empty list or handle as needed

    result = await db.execute(
        select(models.Post)
        .where(models.Post.user_id == user.user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

#Request CRUD
async def create_request(db: AsyncSession, request: schemas.RequestCreate) -> models.Request:
    db_request = models.Request(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_animal)
    return db_request

#Request by ID
async def getRequest(db:AsyncSession, request_id: int) -> Optional[models.Request]:
    result = await db.execute(select(models.Request).where(models.Request.request_id == request_id))
    return result.scalar_one_or_none()

# Get all requests with optional pagination
async def get_requests(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[models.Request]:
    result = await db.execute(select(models.Request).offset(skip).limit(limit))
    return result.scalars().all()

# Update a request
async def update_request(db: AsyncSession, request_id: int, request: schemas.RequestCreate) -> Optional[models.Request]:
    result = await db.execute(select(models.Request).where(models.Request.request_id == request_id))
    db_request = result.scalar_one_or_none()
    if db_request is None:
        return None
    for key, value in request.dict().items():
        setattr(db_request, key, value)
    await db.commit()
    await db.refresh(db_request)
    return db_request

# Delete a request
async def delete_request(db: AsyncSession, request_id: int) -> Optional[models.Request]:
    result = await db.execute(select(models.Request).where(models.Request.request_id == request_id))
    db_request = result.scalar_one_or_none()
    if db_request is None:
        return None
    await db.delete(db_request)
    await db.commit()
    return db_request

#Filter requests by user
async def get_requests_by_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10) -> list[models.Request]:
    result = await db.execute(
        select(models.Request)
        .where(models.Request.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# Get posts by user_id
async def get_posts_by_user_id(db: AsyncSession, user_id: int) -> list[models.Post]:
    result = await db.execute(select(models.Post).where(models.Post.user_id == user_id))
    return result.scalars().all()

# Get posts by email
async def get_posts_by_email(db: AsyncSession, email: str) -> list[models.Post]:
    result = await db.execute(
        select(models.Post).join(models.User).where(models.User.email == email)
    )
    return result.scalars().all()

# Fetching posts by username where the authenticated user has requests
async def get_posts_by_username(db: AsyncSession, username: str, requesting_user_id: int, skip: int = 0, limit: int = 10) -> list[models.Post]:
    user = await get_user_by_username(db, username)
    if not user:
        return []
    
    result = await db.execute(
        select(models.Post)
        .options(joinedload(models.Post.requests))  # Eager load requests
        .join(models.Request, models.Post.post_id == models.Request.post_id)
        .where(
            models.Post.user_id == user.user_id,
            models.Request.user_id == requesting_user_id
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# Fetching posts by email where the authenticated user has requests
async def get_posts_by_email(db: AsyncSession, email: str, requesting_user_id: int, skip: int = 0, limit: int = 10) -> list[models.Post]:
    user = await get_user_by_email(db, email)
    if not user:
        return []

    result = await db.execute(
        select(models.Post)
        .options(joinedload(models.Post.requests))  # Eager load requests
        .join(models.Request, models.Post.post_id == models.Request.post_id)
        .where(
            models.Post.user_id == user.user_id,
            models.Request.user_id == requesting_user_id
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# Fetch posts created by the current user, where the specified username has made requests
async def get_posts_by_user_with_requests(
    db: AsyncSession, 
    username: str, 
    current_user_id: int, 
    skip: int = 0, 
    limit: int = 10
) -> list[models.Post]:
    # Get the user_id of the specified username
    user = await get_user_by_username(db, username)
    if not user:
        return []

    result = await db.execute(
        select(models.Post)
        .options(joinedload(models.Post.requests))  # Eager load requests
        .join(models.Request, models.Post.post_id == models.Request.post_id)
        .where(
            models.Post.user_id == current_user_id,  # Posts by current user
            models.Request.user_id == user.user_id  # Requests by specified username
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()