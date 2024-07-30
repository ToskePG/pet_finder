from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Animal Schemas
class AnimalBase(BaseModel):
    animal_type: str
    animal_breed: str
    animal_name: str
    animal_gender: str
    animal_age: int
    animal_size: str
    animal_coatLength: str
    animal_color: str
    medical_card: str
    location: int
    

class AnimalCreate(AnimalBase):
    pass 

class Animal(AnimalBase):
    animal_id: int
    user_id: int
    class Config:
        orm_mode = True

class AnimalResponse(AnimalBase):
    animal_id: int
    user_id: int
    class Config:
        orm_mode = True

<<<<<<< HEAD
=======
# Existing Schemas
# PetType Schemas
class PetTypeBase(BaseModel):
    pet_type: str

class PetTypeCreate(PetTypeBase):
    pass 

class PetType(PetTypeBase):
    pet_type_id: int
    pet_type: str
    class Config:
        orm_mode = True

class PetTypeResponse(PetTypeBase):
    pet_type_id: int
    pet_type: str
    class Config:
        orm_mode = True

# Pet Schemas
class PetBase(BaseModel):
    pet_type_id: int
    pet_breed: str
    pet_name: str
    pet_gender: str
    pet_age: int
    pet_size: str
    pet_coatLength: str
    pet_color: str
    medical_card: str
    location: int


class PetCreate(PetBase):
    pass 

class Pet(PetBase):
    pet_id: int
    user_id: int
    pet_type: PetType #Include pet type info
    class Config:
        orm_mode = True

class PetResponse(PetBase):
    pet_id: int
    user_id: int
    pet_type: PetType #Include pet type info
    class Config:
        orm_mode = True

class PetUpdate(BaseModel):
    pet_type_id: Optional[int] = None
    pet_breed: Optional[str] = None
    pet_name: Optional[str] = None
    pet_gender: Optional[str] = None
    pet_age: Optional[int] = None
    pet_size: Optional[str] = None
    pet_coatLength: Optional[str] = None
    pet_color: Optional[str] = None
    medical_card: Optional[str] = None
    location: Optional[int] = None

>>>>>>> pet_branch

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str
    is_admin: bool
    
class UserCreate(UserBase):
    password: str
    is_admin: bool = False

class UserResponse(UserBase):
    user_id: int
    username: str
    email: str
    is_admin: bool
<<<<<<< HEAD
    animals: list[Animal] = []

    class Config:
        orm_mode = True

class User(UserBase):
    user_id: int
    animals: list[Animal] = []
    class Config:
        orm_mode = True
=======
    pets: list[Pet] = []

    class Config:
        orm_mode = True

class User(UserBase):
    user_id: int
    pets: list[Pet] = []
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

>>>>>>> pet_branch

# Location Schemas
class LocationBase(BaseModel):
    city_name: str

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    class Config:
        orm_mode = True

class LocationResponse(LocationBase):
    class Config:
        orm_mode = True



# PostType Schemas
class PostTypeBase(BaseModel):
    post_type_name: str

class PostTypeCreate(PostTypeBase):
    pass 

class PostType(PostTypeBase):
    post_type_id: int

    class Config:
        orm_mode = True

# PostTypeResponse Schema
class PostTypeResponse(BaseModel):
    post_type_id: int
    post_type_name: str

    class Config:
        orm_mode = True

# Post Schemas
class PostBase(BaseModel):
    user_id: int
    pet_id: int
    title: str
    abstract: str
    content: str
    image: Optional[bytes]
    post_type_id: int

class CreatePost(PostBase):
    pass 

class Post(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True

# PostResponse Schema
class PostResponse(BaseModel):
    post_id: int
    user_id: int
    pet_id: int
    title: str
    abstract: str
    content: str
    image: Optional[bytes]
    post_type: PostTypeResponse  # Including the post type details
    created_at: datetime

    class Config:
        orm_mode = True

# Request Schemas
class RequestBase(BaseModel):
    user_id: int
    post_id: int
    content: str

class RequestCreate(RequestBase):
    pass

class RequestResponse(RequestBase):
    request_id: int
    user: UserResponse
    post: PostResponse
    content: str

class Request(RequestBase):
    class Config:
        orm_mode = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None