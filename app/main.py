from .Routers import user
from app.database.db import Base, engine
from fastapi import FastAPI
from .database import models

models.Base.metadata.create_all(bind=engine)
app =FastAPI()

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Mount static files if you have any
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user.router)