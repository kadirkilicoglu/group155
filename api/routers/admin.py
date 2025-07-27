from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Base, UserRole, User
from database import engine, SessionLocal
from typing import Annotated

from routers.authentication import get_current_user, bcrypt_context



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
    if user["role_id"] != 1:  # Assuming role 1 is admin
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
    if user["role_id"] != 1:  # Assuming role 1 is admin
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")
    existing_role = session.query(UserRole).filter(UserRole.role_name == role_request.role_name).first()
    if existing_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exists")
    
    role = UserRole(**role_request.model_dump())

    session.add(role)
    session.commit()
    session.refresh(role)
    return role

### Needs to be implemented

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserDep, db : SessionDep, create_user_request: UserRequest):
    """
    Endpoint to create a new user.
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if user["role_id"] != 1:
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

@router.post("/create_user_first_admin", status_code=status.HTTP_201_CREATED)
async def create_user(db : SessionDep, user_request: UserRequest):
    """
    Endpoint to create a new user.
    """
    user = User(
        user_email=user_request.username,
        user_first_name=user_request.first_name,
        user_last_name=user_request.last_name,
        user_role_id=user_request.role,
        user_hashed_password=bcrypt_context.hash(user_request.password)
    )
    db.add(user)
    db.commit()


@router.get("/get_users", status_code=status.HTTP_200_OK)
async def get_users(user: UserDep, session: SessionDep):
    """
    Endpoint to retrieve all users.
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if user["role_id"] != 1:  # Assuming role 1 is admin
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")
    users = session.query(User).all()
    return users