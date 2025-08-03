from fastapi import APIRouter, Depends, HTTPException, Path, status
from request_models import UserRequest, RoleRequest
from sqlalchemy.orm import Session
from models import Base, UserRole, User
from database import engine, SessionLocal
from typing import Annotated, Callable

from routers.authentication import get_current_user, bcrypt_context, require_permission



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


@router.get("/get_roles", status_code=status.HTTP_200_OK)
async def get_roles(user: UserDep, session: SessionDep):
    """
    Endpoint to retrieve all user roles.
    """
    require_permission(user, "can_view_role")
    roles = session.query(UserRole).all()
    return roles
    

@router.post("/create_role", status_code=status.HTTP_201_CREATED)
async def create_role(user: UserDep, role_request: RoleRequest, session: SessionDep):
    """
    Endpoint to create a new user role.
    """
    require_permission(user, "can_create_role")

    existing_role = session.query(UserRole).filter(UserRole.role_name == role_request.role_name).first()
    if existing_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exists")
    
    role = UserRole(**role_request.model_dump())

    session.add(role)
    session.commit()
    session.refresh(role)
    return role


@router.post("/create_role_without_auth", status_code=status.HTTP_201_CREATED)
async def create_role(role_request: RoleRequest, session: SessionDep):
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


@router.put("/update_role/{role_id}", status_code=status.HTTP_200_OK)
async def update_role(user: UserDep, role_id: int, role_request: RoleRequest, session: SessionDep):
    """
    Endpoint to update an existing user role.
    """
    require_permission(user, "can_edit_role")
    existing_role = session.query(UserRole).filter(UserRole.role_id == role_id).first()
    if not existing_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    for key, value in role_request.model_dump().items():
        setattr(existing_role, key, value)
    session.add(existing_role)
    session.commit()
    session.refresh(existing_role)
    return existing_role


@router.delete("/delete_role/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(user: UserDep, role_id: int, session: SessionDep):
    """
    Endpoint to delete an existing user role.
    """
    require_permission(user, "can_delete_role")
    existing_role = session.query(UserRole).filter(UserRole.role_id == role_id).first()
    if not existing_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    
    session.delete(existing_role)
    session.commit()
    return {"detail": "Role deleted successfully"}


@router.delete("/delete_role_without_auth/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, session: SessionDep):
    """
    Endpoint to delete an existing user role.
    """
    existing_role = session.query(UserRole).filter(UserRole.role_id == role_id).first()
    if not existing_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    
    session.delete(existing_role)
    session.commit()
    return {"detail": "Role deleted successfully"}


@router.get("/get_users", status_code=status.HTTP_200_OK)
async def get_users(user: UserDep, session: SessionDep):
    """
    Endpoint to retrieve all users.
    """
    require_permission(user, "can_view_user")
    users = session.query(User).all()
    return users


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserDep, db : SessionDep, create_user_request: UserRequest):
    """
    Endpoint to create a new user.
    """
    require_permission(user, "can_create_user")
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


@router.post("/create_user_without_auth", status_code=status.HTTP_201_CREATED)
async def create_user(db : SessionDep, user_request: UserRequest):
    """
    Endpoint to create the first admin user.
    This endpoint is used to set up the initial admin user for the application.
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


@router.put("/update_user/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user: UserDep, db: SessionDep, user_request: UserRequest, user_id: int = Path(..., description="ID of the user to update", ge=1)):
    """
    Endpoint to update an existing user.
    """
    require_permission(user, "can_edit_user")
    existing_user = db.query(User).filter(User.user_id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for key, value in user_request.model_dump().items():
        setattr(existing_user, key, value)
    db.add(existing_user)
    db.commit()
    db.refresh(existing_user)
    return existing_user


@router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: UserDep, db: SessionDep, user_id: int = Path(..., description="ID of the user to delete", ge=1)):
    """
    Endpoint to delete an existing user.
    """
    require_permission(user, "can_delete_user")
    
    existing_user = db.query(User).filter(User.user_id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(existing_user)
    db.commit()


@router.delete("/delete_user_without_auth/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: SessionDep, user_id: int = Path(..., description="ID of the user to delete", ge=1)):
    """
    Endpoint to delete an existing user.
    """
    
    existing_user = db.query(User).filter(User.user_id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(existing_user)
    db.commit()