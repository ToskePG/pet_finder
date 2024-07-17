from pydantic import BaseModel
from datetime import datetime
from typing import Optional


#User
class UserBase(BaseModel):
    username: str
    email: str
    
    
class UserCreate(UserBase):
    password: str
    
class User(UserBase):

    class Config:
        orm_mode = True

#Animal
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


#Location
class LocationBase(BaseModel):
    city_name: str

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    class Config:
        orm_mode = True


#Animal_type
class AnimalTypeBase(BaseModel):
    animal_type: str

class AnimalTypeCreate(AnimalTypeBase):
    pass 

class AnimalType(AnimalTypeBase):
    class Config:
        orm_mode = True


#Request
class RequestBase(BaseModel):
    user_id: int
    post_id: int
    content: str

class RequestCreate(RequestBase):
    pass 

class Request(RequestBase):
    class Config:
        orm_mode = True


#Post
class PostBase(BaseModel):
    user_id: int
    animal_id: int
    title: str
    abstract: str
    content: str
    image: bytes

class CreatePost(PostBase):
    pass 

class Post(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True
