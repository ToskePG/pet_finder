from .Routers import user
from app.database.db import Base, engine
from fastapi import FastAPI
from .database import models
#Imports for jinja2 templates
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

models.Base.metadata.create_all(bind=engine)
app =FastAPI()

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Mount static files if you have any
app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

app.include_router(user.router)