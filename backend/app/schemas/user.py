"""
User Schemas - Pydantic Models für API Request/Response
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


# Base Schema mit gemeinsamen Feldern
class UserBase(BaseModel):
    """Basis-Felder für User"""
    username: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)


# Schema für User-Erstellung (mit Passwort)
class UserCreate(UserBase):
    """Schema für User-Registrierung"""
    password: str = Field(..., min_length=6, max_length=100)


# Schema für User-Update
class UserUpdate(BaseModel):
    """Schema für User-Update (alle Felder optional)"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    is_active: Optional[bool] = None


# Schema für User-Response (OHNE Passwort!)
class User(UserBase):
    """Schema für User-Response (wird an Frontend geschickt)"""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Schema für User in Listen (minimale Info)
class UserInList(BaseModel):
    """Minimale User-Info für Listen"""
    id: int
    username: str
    name: str

    model_config = ConfigDict(from_attributes=True)


# Schema für Login-Request
class LoginRequest(BaseModel):
    """Schema für Login"""
    username: str
    password: str


# Schema für Token-Response
class Token(BaseModel):
    """Schema für JWT-Token-Response"""
    access_token: str
    token_type: str = "bearer"


# Schema für Token-Payload
class TokenData(BaseModel):
    """Schema für Token-Payload"""
    username: Optional[str] = None
