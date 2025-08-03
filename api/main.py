from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Base
from database import engine
from routers.prediction import router as prediction_router
from routers.admin import router as admin_router
from routers.authentication import router as authentication_router
from routers.patient import router as patient_router
from routers.entry import router as entry_router
from contextlib import asynccontextmanager
from pathlib import Path
from keras.models import load_model
import joblib

BASE_DIR = Path(__file__).resolve().parent
PREDICTION_MODEL_DIR = (BASE_DIR / "../prediction_model").resolve()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Dosya yollarını dinamik al
    scaler_path = PREDICTION_MODEL_DIR / "scaler.pkl"
    model_path = PREDICTION_MODEL_DIR / "triage_model.h5"

    app.state.scaler = joblib.load(scaler_path)
    app.state.triage_model = load_model(model_path)

    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

# Statik dosya ve template dizinlerini ayarla
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Sayfa endpointleri (her endpoint ismi farklı olmalı!)
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("main-page.html", {"request": request})

@app.get("/patient-page", response_class=HTMLResponse)
def patient_page(request: Request):
    return templates.TemplateResponse("patient-page.html", {"request": request})

@app.get("/patient-info-page", response_class=HTMLResponse)
def patient_info_page(request: Request):
    return templates.TemplateResponse("patient-info-page.html", {"request": request})

@app.get("/main-page", response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse("main-page.html", {"request": request})

@app.get("/doctor-page", response_class=HTMLResponse)
def doctor_page(request: Request):
    return templates.TemplateResponse("doctor-page.html", {"request": request})

@app.get("/patient-list-page", response_class=HTMLResponse)
def patient_list_page(request: Request):
    return templates.TemplateResponse("patient-list-page.html", {"request": request})

# Router'ları ekle
app.include_router(prediction_router)
app.include_router(admin_router)
app.include_router(authentication_router)
app.include_router(patient_router)
app.include_router(entry_router)