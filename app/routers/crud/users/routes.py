from app.routers import schemas
from app.routers.crud.users import users
from typing import List, Optional

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db

router = APIRouter(prefix="", tags=["Authentication"])

@router.post("/signup", tags=["Authentication"])
def signup(signup: schemas.Signup, db: Session = Depends(get_db)):
    data = users.sign_up(db=db, signup=signup)
    return "User Created"


@router.post("/login", response_model=schemas.LoginResponse, tags=["Authentication"])
def login(login: schemas.Login, db: Session = Depends(get_db)):
    data = users.login(db=db, login=login)
    return data