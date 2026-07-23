import re
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional


def validate_email_str(email: str) -> str:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")
    return email


class UserCreate(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User plain password")

    @field_validator('email')
    def validate_email(cls, v):
        return validate_email_str(v)


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator('email')
    def validate_email(cls, v):
        return validate_email_str(v)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class CourseCreate(BaseModel):
    title: str
    code: str
    department: str
    credits: int = 3


class CourseResponse(BaseModel):
    id: int
    title: str
    code: str
    department: str
    credits: int

    model_config = ConfigDict(from_attributes=True)
