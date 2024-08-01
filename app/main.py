from app.database.db import Base, engine
from .Routers import user, post, location, pet
from .database.db import Base, engine
from fastapi import FastAPI
from .database import models
#Imports for jinja2 templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
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

#Loads favicon, hate that 404 error lol
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url='app/static/favicon.png')

app.include_router(user.router, prefix="/api/users")
app.include_router(pet.router, prefix="/api/pets")
app.include_router(post.router, prefix="/api/posts")