from app.database.db import Base, engine
from .Routers import user, post, location, pet
from .database.db import Base, engine
from fastapi import FastAPI
from .database import models
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
#Imports for jinja2 templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

models.Base.metadata.create_all(bind=engine)
app =FastAPI()

# Setup CORS
origins = [
    "http://localhost",        # Frontend on the same machine, different port
    "http://localhost:3000",   # Common port for React
    "http://yourfrontend.com", # Your actual frontend domain
    # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows only specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

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
app.include_router(location.router, prefix="/api/location")