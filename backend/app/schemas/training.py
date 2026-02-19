"""
Training & Exercise Schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime


# Exercise Schemas
class ExerciseBase(BaseModel):
    """Basis-Felder für Exercise"""
    name: str = Field(..., min_length=1, max_length=200)
    sets: Optional[int] = Field(None, ge=1, le=100)
    reps: Optional[int] = Field(None, ge=1, le=1000)
    weight: Optional[float] = Field(None, ge=0, le=1000)
    notes: Optional[str] = None
    order: int = Field(0, ge=0)


class ExerciseCreate(ExerciseBase):
    """Schema für Exercise-Erstellung"""
    pass


class ExerciseUpdate(BaseModel):
    """Schema für Exercise-Update"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    sets: Optional[int] = Field(None, ge=1, le=100)
    reps: Optional[int] = Field(None, ge=1, le=1000)
    weight: Optional[float] = Field(None, ge=0, le=1000)
    notes: Optional[str] = None
    order: Optional[int] = Field(None, ge=0)


class Exercise(ExerciseBase):
    """Schema für Exercise-Response"""
    id: int
    training_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Training Schemas
class TrainingBase(BaseModel):
    """Basis-Felder für Training"""
    date: date
    title: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, ge=1, le=600)


class TrainingCreate(TrainingBase):
    """Schema für Training-Erstellung"""
    exercises: List[ExerciseCreate] = []


class TrainingUpdate(BaseModel):
    """Schema für Training-Update"""
    date: Optional[date] = None
    title: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, ge=1, le=600)


class Training(TrainingBase):
    """Schema für Training-Response"""
    id: int
    user_id: int
    exercises: List[Exercise] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TrainingInList(BaseModel):
    """Minimale Training-Info für Listen (ohne Exercises)"""
    id: int
    user_id: int
    date: date
    title: Optional[str] = None
    duration_minutes: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
