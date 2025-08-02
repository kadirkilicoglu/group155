from fastapi import APIRouter, Depends, HTTPException, Path, status, Request, Form
from starlette import status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Base, UserRole, User
from database import engine, SessionLocal
from typing import Annotated

from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone

from jose import jwt, JWTError

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

import os

templates = Jinja2Templates(directory=os.path.join("api", "templates"))


router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"]
)

load_dotenv()

# Constants for JWT token creation
# Moved to a separate config file or environment variables in production
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_session)]


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/authentication/token")


class Token(BaseModel):
    access_token: str
    token_type: str


class UserRoleRequest(BaseModel):

    role_name: str = Field(..., example="Admin", description="Name of the user role", min_length=1, max_length=50)
    role_description: str = Field(..., example="Administrator with full access", description="Description of the user role", min_length=1, max_length=255, nullable=True)

    can_create_user: bool = Field(default=False, example=True, description="Permission to create a user")
    can_edit_user: bool = Field(default=False, example=True, description="Permission to edit a user")
    can_delete_user: bool = Field(default=False, example=True, description="Permission to delete a user")
    can_view_user: bool = Field(default=False, example=True, description="Permission to view a user")

    can_create_role: bool = Field(default=False, example=True, description="Permission to create a user role")
    can_edit_role: bool = Field(default=False, example=True, description="Permission to edit a user role")
    can_delete_role: bool = Field(default=False, example=True, description="Permission to delete a user role")
    can_view_role: bool = Field(default=False, example=True, description="Permission to view a user role")

    can_create_patient: bool = Field(default=False, example=True, description="Permission to create a patient")
    can_edit_patient: bool = Field(default=False, example=True, description="Permission to edit a patient")
    can_delete_patient: bool = Field(default=False, example=True, description="Permission to delete a patient")
    can_view_patient: bool = Field(default=False, example=True, description="Permission to view a patient")

    can_create_entry: bool = Field(default=False, example=True, description="Permission to create an entry")
    can_edit_entry: bool = Field(default=False, example=True, description="Permission to edit an entry")
    can_delete_entry: bool = Field(default=False, example=True, description="Permission to delete an entry")
    can_view_entry: bool = Field(default=False, example=True, description="Permission to view an entry")

    can_create_prediction: bool = Field(default=False, example=True, description="Permission to create a prediction")
    can_edit_prediction: bool = Field(default=False, example=True, description="Permission to edit a prediction")
    can_delete_prediction: bool = Field(default=False, example=True, description="Permission to delete a prediction")
    can_view_prediction: bool = Field(default=False, example=True, description="Permission to view a prediction")

    can_create_feedback: bool = Field(default=False, example=True, description="Permission to create feedback")
    can_edit_feedback: bool = Field(default=False, example=True, description="Permission to edit feedback")
    can_delete_feedback: bool = Field(default=False, example=True, description="Permission to delete feedback")
    can_view_feedback: bool = Field(default=False, example=True, description="Permission to view feedback")

    can_create_report: bool = Field(default=False, example=True, description="Permission to create a report")
    can_edit_report: bool = Field(default=False, example=True, description="Permission to edit a report")
    can_delete_report: bool = Field(default=False, example=True, description="Permission to delete a report")
    can_view_report: bool = Field(default=False, example=True, description="Permission to view a report")


def require_permission(user: dict, permission: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    permissions = user.get("user_role", {})
    if not permissions.get(permission, False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission '{permission}' is required to access this resource"
        )


def create_acces_token(username: str, user_id: int, user_role: UserRoleRequest, expires_delta: timedelta):
    """
    Create a JWT access token.
    """
    payload = {"sub": username, "id": user_id, "user_role": user_role.model_dump()}
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({"exp": expires})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(username: str, password: str, db: SessionDep):
    """
    Authenticate a user by checking the username and password.
    """
    #user = db.query(User).filter(User.user_email == username).first()
    user = db.query(User).join(User.role).filter(User.user_email == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.user_hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Get the current user from the JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role_dict: dict = payload.get("user_role")
        user_role: UserRoleRequest = UserRoleRequest(**user_role_dict)
        if username is None or user_id is None or user_role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "user_id": user_id, "user_role": user_role.model_dump()}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/token", response_model = Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: SessionDep):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_acces_token(
        username=user.user_email,
        user_id=user.user_id,
        user_role=UserRoleRequest(**user.role.__dict__),
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_session)):
    user = db.query(User).filter(User.user_email == email).first()

    if not user or not bcrypt_context.verify(password, user.user_hashed_password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Email veya şifre hatalı"
        })

    role = db.query(UserRole).filter(UserRole.role_id == user.user_role_id).first()

    if role and role.role_name == "admin":
        return RedirectResponse(url="/authentication/admin-page", status_code=303)

    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Yetersiz yetki"
    })

@router.get("/admin-page")
async def admin_page(request: Request):
    return templates.TemplateResponse("admin-page.html", {"request": request})