from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Base, UserRole, User
from database import engine, SessionLocal
from typing import Annotated


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_session)]


class UserRoleRequest(BaseModel):
    role_name: str = Field(..., example="Admin", description="Name of the user role", min_length=1, max_length=50)
    role_description: str = Field(..., example="Administrator with full access", description="Description of the user role", min_length=1, max_length=255, nullable=True)


@router.get("/get_user_roles", status_code=status.HTTP_200_OK)
async def get_user_roles(session: SessionDep):
    """
    Endpoint to retrieve all user roles.
    """
    roles = session.query(UserRole).all()
    return roles


@router.post("/create_user_role", status_code=status.HTTP_201_CREATED)
async def create_user_role(role_request: UserRoleRequest, session: SessionDep):
    """
    Endpoint to create a new user role.
    """
    existing_role = session.query(UserRole).filter(UserRole.role_name == role_request.role_name).first()
    if existing_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exists")
    
    role = UserRole(**role_request.model_dump())

    session.add(role)
    session.commit()
    session.refresh(role)
    return role