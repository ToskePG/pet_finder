
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
    is_confirmed = Column(Boolean, default=False)
    pets = relationship("Pet", cascade = "all, delete-orphan")
    posts = relationship('Post', cascade = "all, delete-orphan")

    @staticmethod
    def validate_email(email):
        email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return re.match(email_regex, email) is not None

class Pet(Base):
    __tablename__ = 'pets'

    pet_id = Column(Integer, primary_key=True)
    pet_type_id = Column(Integer, ForeignKey("pet_types.pet_type_id"), nullable= False)
    pet_breed = Column(String, nullable= False)
    pet_name = Column(String, nullable= False)
    pet_gender = Column(String, nullable= False)
    pet_age = Column(Integer, nullable= False)
    pet_size = Column(String, nullable= False)
    pet_coatLength = Column(String, nullable= False)
    pet_color = Column(String, nullable= False)
    medical_card = Column(String)
    location = Column(Integer, ForeignKey("locations.location_id"), nullable= False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable= False)

    pet_type = relationship("PetType")

class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True)
    city_name = Column(String, unique=True)
    
class PetType(Base):
    __tablename__ = "pet_types"
    
    pet_type_id = Column(Integer, primary_key=True)
    pet_type = Column(String, unique=True)

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    pet_id = Column(Integer, ForeignKey("pets.pet_id"))
    title = Column(String)
    abstract = Column(String)
    content = Column(String)
    image = Column(LargeBinary)

    user = relationship("User", back_populates="posts")
    pet = relationship("Pet")