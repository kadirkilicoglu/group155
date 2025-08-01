from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from .models import Base
from .database import engine
from .routers.prediction import router as prediction_router
from .routers.admin import router as admin_router
from .routers.authentication import router as authentication_router
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)
    #ml_models[""] = ml_models.load_model("path/to/model")
    yield

    #ml_models.clear()


app = FastAPI(lifespan = lifespan)

app.mount("/static", StaticFiles(directory=os.path.join("api", "static")), name="static")
templates = Jinja2Templates(directory=os.path.join("api", "templates"))

#Ana sayfa yönlendirmesi
@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("main-page.html", {"request": request})

app.include_router(prediction_router)
app.include_router(admin_router)
app.include_router(authentication_router)