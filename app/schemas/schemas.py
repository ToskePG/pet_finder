from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Existing Schemas

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str
    is_admin: bool
    
class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    class Config:
        orm_mode = True

# Animal Schemas
class AnimalBase(BaseModel):
    animal_type: str
    animal_breed: str
    medical_card: str
    location: int

class AnimalCreate(AnimalBase):
    pass 

class Animal(AnimalBase):
    class Config:
        orm_mode = True

# Location Schemas
class LocationBase(BaseModel):
    city_name: str

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    class Config:
        orm_mode = True

# AnimalType Schemas
class AnimalTypeBase(BaseModel):
    animal_type: str

class AnimalTypeCreate(AnimalTypeBase):
    pass 

class AnimalType(AnimalTypeBase):
    class Config:
        orm_mode = True

# Request Schemas
class RequestBase(BaseModel):
    user_id: int
    post_id: int
    content: str

class RequestCreate(RequestBase):
    pass 

class Request(RequestBase):
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

# New Schemas

# PostTypeResponse Schema
class PostTypeResponse(BaseModel):
    post_type_id: int
    post_type_name: str

    class Config:
        orm_mode = True

# Post Schemas
class PostBase(BaseModel):
    user_id: int
    animal_id: int
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
    animal_id: int
    title: str
    abstract: str
    content: str
    image: Optional[bytes]
    post_type: PostTypeResponse  # Including the post type details
    created_at: datetime

    class Config:
        orm_mode = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
