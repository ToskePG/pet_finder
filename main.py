from .Routers import user
from .db import Base, engine
from fastapi import FastAPI
from . import models

models.Base.metadata.create_all(bind=engine)
app =FastAPI()

app.include_router(user.router)