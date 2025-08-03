from fastapi import APIRouter, Depends, HTTPException, Path, status, Form
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload
from api.models import Entry
from api.request_models import EntryRequest
from api.database import SessionLocal
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from api.routers.authentication import get_current_user, require_permission

router = APIRouter(
    prefix="/entry",
    tags=["Entry"]
)

templates = Jinja2Templates(directory="api/routers/templates")

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_session)]
UserDep = Annotated[dict, Depends(get_current_user)]

@router.get("/get_entries", status_code=status.HTTP_200_OK)
async def get_entries(user: UserDep, session: SessionDep):
    require_permission(user, "can_view_entry")

    query = session.query(Entry).options(joinedload(Entry.patient))

    if user["user_role"]["role_id"] == 3:
        query = query.filter(Entry.entry_assigned_doctor_id == user["user_id"])

    entries = query.all()

    entry_list = []
    for entry in entries:
        entry_dict = entry.__dict__.copy()
        entry_dict.pop('_sa_instance_state', None)
        if entry.patient:
            entry_dict["patient"] = {
                "patient_first_name": entry.patient.patient_first_name,
                "patient_last_name": entry.patient.patient_last_name,
            }
        else:
            entry_dict["patient"] = None
        entry_list.append(entry_dict)

    return entry_list

@router.get("/get_entry/{entry_id}", status_code=status.HTTP_200_OK)
async def get_entry(entry_id: int, user: UserDep, session: SessionDep):
    require_permission(user, "can_view_entry")
    entry = session.query(Entry)\
        .options(
            joinedload(Entry.patient),
            joinedload(Entry.model_predictions)
        )\
        .filter(Entry.entry_id == entry_id).first()
    
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")

    entry_dict = entry.__dict__.copy()
    entry_dict.pop("_sa_instance_state", None)

    if entry.patient:
        entry_dict["patient"] = {
            "patient_first_name": entry.patient.patient_first_name,
            "patient_last_name": entry.patient.patient_last_name,
            "patient_gender": entry.patient.patient_gender,
            "patient_birth_date": entry.patient.patient_birth_date,
        }

    if entry.model_predictions:
        entry_dict["model_predictions"] = [
            {"prediction_label": p.prediction_label}
            for p in entry.model_predictions
        ]
    else:
        entry_dict["model_predictions"] = []

    return entry_dict

@router.post("/create_entry", status_code=status.HTTP_201_CREATED)
async def create_entry(user: UserDep, entry_request: EntryRequest, session: SessionDep):
    require_permission(user, "can_create_entry")
    entry = Entry(**entry_request.model_dump())
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry

@router.put("/update_entry/{entry_id}", status_code=status.HTTP_200_OK)
async def update_entry(entry_id: int, user: UserDep, entry_request: EntryRequest, session: SessionDep):
    require_permission(user, "can_update_entry")
    entry = session.query(Entry).filter(Entry.entry_id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    
    for key, value in entry_request.model_dump().items():
        setattr(entry, key, value)
    
    session.commit()
    session.refresh(entry)
    return entry

@router.delete("/delete_entry/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entry(entry_id: int, user: UserDep, session: SessionDep):
    require_permission(user, "can_delete_entry")
    entry = session.query(Entry).filter(Entry.entry_id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    
    session.delete(entry)
    session.commit()
    return {"detail": "Entry deleted successfully"}
