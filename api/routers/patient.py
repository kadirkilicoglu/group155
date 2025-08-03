from fastapi import APIRouter, Depends, HTTPException, Path, status, Form
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Base, UserRole, User, Patient
from request_models import PatientRequest
from database import engine, SessionLocal
from typing import Annotated, Callable
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from routers.authentication import get_current_user, require_permission


router = APIRouter(
    prefix="/patient",
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


router = APIRouter()
templates = Jinja2Templates(directory="api/routers/templates")


@router.get("/check")
def check_patient(email: str, db: Session = Depends(get_session)):
    patient = db.query(Patient).filter(Patient.patient_email == email).first()
    if patient:
        return {"exists": True}
    return {"exists": False}


@router.get("/get_patients", status_code=status.HTTP_200_OK)
async def get_patients(user: UserDep, session: SessionDep):
    """
    Endpoint to retrieve all patients.
    """
    require_permission(user, "can_view_patient")
    patients = session.query(Patient).all()
    return patients


@router.get("/get_patient/{patient_id}", status_code=status.HTTP_200_OK)
async def get_patient(patient_id: int, user: UserDep, session: SessionDep):
    """
    Endpoint to retrieve a specific patient by ID.
    """
    require_permission(user, "can_view_patient")
    patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    return patient


@router.put("/update_patient/{patient_id}", status_code=status.HTTP_200_OK)
async def update_patient(patient_id: int, user: UserDep, patient_request: PatientRequest, session: SessionDep):
    """
    Endpoint to update an existing patient.
    """
    require_permission(user, "can_edit_patient")

    existing_patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()

    if not existing_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    for key, value in patient_request.model_dump().items():
        setattr(existing_patient, key, value)

    session.commit()
    session.refresh(existing_patient)

    return existing_patient


@router.delete("/delete_patient/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int, user: UserDep, session: SessionDep):
    """
    Endpoint to delete an existing patient.
    """
    require_permission(user, "can_delete_patient")
    existing_patient = session.query(Patient).filter(Patient.patient_id == patient_id).first()

    if not existing_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    session.delete(existing_patient)
    session.commit()
    return {"detail": "Patient deleted successfully"}


# Hasta kaydı
@router.post("/patients/register")
def register_patient(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    birth_year: str = Form(...),
    gender: str = Form(...),
    db: Session = Depends(get_session)
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
