from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.models import Base
from api.database import engine
from api.routers.prediction import router as prediction_router
from api.routers.admin import router as admin_router
from api.routers.authentication import router as authentication_router
from api.routers.patient import router as patient_router
from contextlib import asynccontextmanager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("main-page.html", {"request": request})

@app.get("/patient-page", response_class=HTMLResponse)
def get_patient_page(request: Request):
    return templates.TemplateResponse("patient-page.html", {"request": request})

@app.get("/patient-info-page", response_class=HTMLResponse)
def get_patient_info_page(request: Request):
    return templates.TemplateResponse("patient-info-page.html", {"request": request})


@app.get("/main-page", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("main-page.html", {"request": request})

@app.get("/doctor-page", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("doctor-page.html", {"request": request})

app.include_router(prediction_router)
app.include_router(admin_router)
app.include_router(authentication_router)
app.include_router(patient_router)
