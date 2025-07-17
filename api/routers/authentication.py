from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Base, UserRole, User
from database import engine, SessionLocal
from typing import Annotated


router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"]
)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/login", response_model=User)
async def login():
    """
    Endpoint to handle user login.
    This is a placeholder function and should be implemented with actual logic.
    """
    return {"message": "This endpoint will handle user login."}