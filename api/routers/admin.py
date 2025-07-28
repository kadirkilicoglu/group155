from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Base, UserRole, User
from database import engine, SessionLocal
from typing import Annotated

from routers.authentication import get_current_user, bcrypt_context

import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID"))



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
UserDep = Annotated[dict, Depends(get_current_user)]


class UserRoleRequest(BaseModel):
    role_name: str = Field(..., example="Admin", description="Name of the user role", min_length=1, max_length=50)
    role_description: str = Field(..., example="Administrator with full access", description="Description of the user role", min_length=1, max_length=255, nullable=True)


class UserRequest(BaseModel):
    username : str
    first_name : str
    last_name : str
    password : str
    role : int


@router.get("/get_user_roles", status_code=status.HTTP_200_OK)
async def get_user_roles(user: UserDep, session: SessionDep):
    """
    Endpoint to retrieve all user roles.
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if user["role_id"] != ADMIN_ROLE_ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")
    roles = session.query(UserRole).all()
    return roles


@router.post("/create_user_role", status_code=status.HTTP_201_CREATED)
async def create_user_role(user: UserDep, role_request: UserRoleRequest, session: SessionDep):
    """
    Endpoint to create a new user role.
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if user["role_id"] != ADMIN_ROLE_ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")
    existing_role = session.query(UserRole).filter(UserRole.role_name == role_request.role_name).first()
    if existing_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exists")
    
    role = UserRole(**role_request.model_dump())

    session.add(role)
    session.commit()
    session.refresh(role)
    return role


@router.get("/get_users", status_code=status.HTTP_200_OK)
async def get_users(user: UserDep, session: SessionDep):
    """
    Endpoint to retrieve all users.
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if user["role_id"] != ADMIN_ROLE_ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")
    users = session.query(User).all()
    return users


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserDep, db : SessionDep, create_user_request: UserRequest):
    """
    Endpoint to create a new user.
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if user["role_id"] != ADMIN_ROLE_ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")
    
    existing_user = db.query(User).filter(User.user_email == create_user_request.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    user = User(
        user_email=create_user_request.username,
        user_first_name=create_user_request.first_name,
        user_last_name=create_user_request.last_name,
        user_role_id=create_user_request.role,
        user_hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(user)
    db.commit()


#@router.post("/create_user_first_admin", status_code=status.HTTP_201_CREATED)
#async def create_user(db : SessionDep, user_request: UserRequest):
    """
    Endpoint to create the first admin user.
    This endpoint is used to set up the initial admin user for the application.
    """
    #user = User(
        #user_email=user_request.username,
        #user_first_name=user_request.first_name,
        #user_last_name=user_request.last_name,
        #user_role_id=user_request.role,
        #user_hashed_password=bcrypt_context.hash(user_request.password)
    #)
    #db.add(user)
    #db.commit()


@router.put("/update_user/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user: UserDep, db: SessionDep, user_request: UserRequest, user_id: int = Path(..., description="ID of the user to update", ge=1)):
    """
    Endpoint to update an existing user.
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if user["role_id"] != ADMIN_ROLE_ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")
    
    existing_user = db.query(User).filter(User.user_id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user_request.first_name:
        existing_user.user_first_name = user_request.first_name
    if user_request.last_name:
        existing_user.user_last_name = user_request.last_name
    if user_request.role:
        if not db.query(UserRole).filter(UserRole.role_id == user_request.role).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role does not exist")    
        existing_user.user_role_id = user_request.role
    if user_request.password:
        existing_user.user_hashed_password = bcrypt_context.hash(user_request.password)
    
    db.add(existing_user)
    db.commit()

    db.refresh(existing_user)


@router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: UserDep, db: SessionDep, user_id: int = Path(..., description="ID of the user to delete", ge=1)):
    """
    Endpoint to delete an existing user.
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if user["role_id"] != ADMIN_ROLE_ID:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")
    
    existing_user = db.query(User).filter(User.user_id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(existing_user)
    db.commit()