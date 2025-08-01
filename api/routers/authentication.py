from fastapi import APIRouter, Depends, HTTPException, Path, status, Request, Form
from starlette import status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..models import Base, UserRole, User
from ..database import engine, SessionLocal
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


def create_acces_token(username: str, user_id: int, role: int, expires_delta: timedelta):
    """
    Create a JWT access token.
    """
    payload = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({"exp": expires})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(username: str, password: str, db: SessionDep):
    """
    Authenticate a user by checking the username and password.
    """
    user = db.query(User).filter(User.user_email == username).first()
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
        user_role: int = payload.get("role")
        if username is None or user_id is None or user_role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "user_id": user_id, "role_id": user_role}
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
        role=user.user_role_id,
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