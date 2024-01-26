from datetime import datetime
from typing import List, Optional

from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, validator


class Signup(BaseModel):
    name: str
    email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=50)

    @validator("email")
    def valid_email(cls, email):
        try:
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )


class Login(BaseModel):
    email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=100)

    @validator("email")
    def valid_email(cls, email):
        try:
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )


class Users(BaseModel):
    id: str
    name: str
    email: str


class LoginResponse(Users):
    token: Optional[str]
