
from ..database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Boolean, LargeBinary
from sqlalchemy.orm import relationship
import re


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username= Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)
    password = Column(String)
    animals = relationship("Animal")


    @staticmethod
    def validate_email(email):
        email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return re.match(email_regex, email) is not None

class Animal(Base):
    __tablename__ = 'animals'

    animal_id = Column(Integer, primary_key=True)
    animal_type = Column(String, ForeignKey("animal_types.animal_type_id"))
    animal_breed = Column(String)
    animal_name = Column(String)
    animal_gender = Column(String)
    animal_age = Column(Integer)
    animal_size = Column(String)
    animal_coatLength = Column(String)
    animal_color = Column(String)
    medical_card = Column(String)
    location = Column(Integer, ForeignKey("locations.location_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))

class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True)
    city_name = Column(String, unique=True)
    
class Animal_type(Base):
    __tablename__ = "animal_types"
    
    animal_type_id = Column(Integer, primary_key=True)
    animal_type = Column(String, unique=True)

class Request(Base):
    __tablename__ = "requests"

    request_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    content = Column(String)

class PostType(Base):
    __tablename__ = "post_types"

    post_type_id = Column(Integer, primary_key=True)
    post_type_name = Column(String, unique=True)

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    animal_id = Column(Integer, ForeignKey("animals.animal_id"))
    title = Column(String)
    abstract = Column(String)
    content = Column(String)
    image = Column(LargeBinary)
    created_at = Column(Date)
    request_id = Column(Integer, ForeignKey("requests.request_id"))
    post_type_id = Column(Integer, ForeignKey("post_types.post_type_id"), nullable=False)

    user = relationship("User", back_populates="posts")
    animal = relationship("Animal")
    post_type = relationship("PostType")

User.posts = relationship("Post", order_by=Post.post_id, back_populates="user")