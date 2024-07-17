from .Routers import user
from app.database.db import Base, engine
from fastapi import FastAPI
from .database import models

models.Base.metadata.create_all(bind=engine)
app =FastAPI()

app.include_router(user.router)