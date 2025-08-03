# from fastapi import APIRouter, Depends, HTTPException, Path, status
# from pydantic import BaseModel, Field
# from sqlalchemy.orm import Session
# from models import Base, UserRole, User
# from database import engine, SessionLocal
# from typing import Annotated, Callable

# from routers.authentication import get_current_user, require_permission

# router = APIRouter(
#     prefix="/patient",
#     tags=["Patient"]
# )

# def get_session():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# SessionDep = Annotated[Session, Depends(get_session)]
# UserDep = Annotated[dict, Depends(get_current_user)]


from fastapi import APIRouter, Request, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import Patient
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="api/routers/templates")

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Hasta girişi kontrolü
@router.get("/patients/check")
def check_patient(email: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.patient_email == email).first()
    if patient:
        return {"exists": True}
    return {"exists": False}

# Hasta kaydı
@router.post("/patients/register")
def register_patient(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    birth_year: str = Form(...),
    gender: str = Form(...),
    db: Session = Depends(get_db)
):
    existing = db.query(Patient).filter(Patient.patient_email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı.")

    new_patient = Patient(
        patient_first_name=first_name,
        patient_last_name=last_name,
        patient_email=email,
        patient_birth_date=birth_year,
        patient_gender=gender
    )
    db.add(new_patient)
    db.commit()
    return RedirectResponse("/patient-info-page", status_code=303)
