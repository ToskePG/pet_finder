from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# PetType Schemas
class PetTypeBase(BaseModel):
    pet_type: str

class PetTypeCreate(PetTypeBase):
    pass 

class PetType(PetTypeBase):
    pet_type_id: int
    pet_type: str
    class Config:
        from_attributes = True

class PetTypeResponse(PetTypeBase):
    pet_type_id: int
    pet_type: str
    class Config:
        from_attributes = True

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
    pet_type: PetType  # Include pet type info
    class Config:
        from_attributes = True

class PetResponse(PetBase):
    pet_id: int
    user_id: int
    pet_type: PetType  # Include pet type info
    class Config:
        from_attributes = True

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

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str
    
class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: int
    username: str
    email: str
    is_admin: bool
    is_confirmed: bool  # Include is_confirmed
    pets: list[Pet] = []

    class Config:
        from_attributes = True

class User(UserBase):
    user_id: int
    is_admin: bool
    is_confirmed: bool  # Include is_confirmed
    pets: list[Pet] = []
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

# Location Schemas
class LocationBase(BaseModel):
    city_name: str

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    class Config:
        from_attributes = True

class LocationResponse(LocationBase):
    class Config:
        from_attributes = True

# PostType Schemas
class PostTypeBase(BaseModel):
    type_name: str

class PostTypeCreate(PostTypeBase):
    pass

class PostType(PostTypeBase):
    post_type_id: int
    class Config:
        from_attributes = True

# Post Schemas
class PostBase(BaseModel):
    user_id: int
    pet_id: int
    post_type: Optional[PostType]  # Include post_type in PostBase
    title: str
    abstract: str
    content: str
    image: Optional[bytes]

class CreatePost(PostBase):
    pass 

class Post(PostBase):
    created_at: datetime
    class Config:
        from_attributes = True

# PostResponse Schema
class PostResponse(BaseModel):
    post_id: int
    user_id: int
    pet_id: int
    post_type: Optional[PostType]  # Include post_type in PostResponse
    title: str
    abstract: str
    content: str
    image: Optional[bytes]

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
