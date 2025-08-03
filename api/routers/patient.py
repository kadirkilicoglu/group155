from fastapi import APIRouter, Depends, HTTPException, Form, status
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import Annotated

from api.models import Patient
from api.request_models import PatientRequest
from api.database import SessionLocal
from api.routers.authentication import get_current_user, require_permission

router = APIRouter(
    prefix="/patients",
    tags=["Patient"]
)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_session)]
UserDep = Annotated[dict, Depends(get_current_user)]

@router.get("/check")
def check_patient(email: str, db: Session = Depends(get_session)):
    exists = bool(
        db.query(Patient)
          .filter(Patient.patient_email == email)
          .first()
    )
    return {"exists": exists}

@router.get("/get_by_email", status_code=status.HTTP_200_OK)
def get_patient_by_email(email: str, db: Session = Depends(get_session)):
    patient = db.query(Patient).filter(Patient.patient_email == email).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return {
        "first_name": patient.patient_first_name,
        "last_name": patient.patient_last_name,
        "email": patient.patient_email,
        "birth_year": patient.patient_birth_date,
        "gender": patient.patient_gender
    }

@router.post("/register")
def register_patient(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    birth_year: str = Form(...),
    gender: str = Form(...),
    db: Session = Depends(get_session)
):
    if db.query(Patient).filter(Patient.patient_email == email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu e-posta zaten kayıtlı.")
    new_patient = Patient(
        patient_first_name=first_name,
        patient_last_name=last_name,
        patient_email=email,
        patient_birth_date=birth_year,
        patient_gender=gender
    )
    db.add(new_patient)
    db.commit()
    return RedirectResponse(url="/patient-info-page", status_code=status.HTTP_303_SEE_OTHER)