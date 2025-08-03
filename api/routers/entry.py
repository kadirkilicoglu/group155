from fastapi import APIRouter, Depends, HTTPException, Path, status, Form
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Base, Entry
from request_models import EntryRequest
from database import SessionLocal
from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from routers.authentication import get_current_user, require_permission


router = APIRouter(
    prefix="/entry",
    tags=["Entry"]
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


@router.get("/get_entries", status_code=status.HTTP_200_OK)
async def get_entries(user: UserDep, session: SessionDep):
    """
    Endpoint to retrieve all entries.
    """
    require_permission(user, "can_view_entry")
    entries = session.query(Entry).all()
    return entries


@router.get("/get_entry/{entry_id}", status_code=status.HTTP_200_OK)
async def get_entry(entry_id: int, user: UserDep, session: SessionDep):
    """
    Endpoint to retrieve a specific entry by ID.
    """
    require_permission(user, "can_view_entry")
    entry = session.query(Entry).filter(Entry.entry_id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    return entry


@router.post("/create_entry", status_code=status.HTTP_201_CREATED)
async def create_entry(user: UserDep, entry_request: EntryRequest, session: SessionDep):
    """
    Endpoint to create a new entry.
    """
    require_permission(user, "can_create_entry")
    
    entry = Entry(**entry_request.model_dump())

    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


@router.put("/update_entry/{entry_id}", status_code=status.HTTP_200_OK)
async def update_entry(entry_id: int, user: UserDep, entry_request: EntryRequest, session: SessionDep):
    """
    Endpoint to update an existing entry by ID.
    """
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
    """ 
    Endpoint to delete an existing entry by ID.
    """
    require_permission(user, "can_delete_entry")
    entry = session.query(Entry).filter(Entry.entry_id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    
    session.delete(entry)
    session.commit()
    return {"detail": "Entry deleted successfully"}