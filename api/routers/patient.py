from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Base, UserRole, User
from database import engine, SessionLocal
from typing import Annotated, Callable

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