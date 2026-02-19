"""
Meal Schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from app.models.meal import MealType


class MealBase(BaseModel):
    """Basis-Felder für Meal"""
    date: date
    meal_type: MealType
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    calories: Optional[int] = Field(None, ge=0, le=10000)
    protein: Optional[float] = Field(None, ge=0, le=1000)  # g
    carbs: Optional[float] = Field(None, ge=0, le=2000)  # g
    fat: Optional[float] = Field(None, ge=0, le=500)  # g


class MealCreate(MealBase):
    """Schema für Meal-Erstellung"""
    pass


class MealUpdate(BaseModel):
    """Schema für Meal-Update"""
    date: Optional[date] = None
    meal_type: Optional[MealType] = None
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    calories: Optional[int] = Field(None, ge=0, le=10000)
    protein: Optional[float] = Field(None, ge=0, le=1000)
    carbs: Optional[float] = Field(None, ge=0, le=2000)
    fat: Optional[float] = Field(None, ge=0, le=500)


class Meal(MealBase):
    """Schema für Meal-Response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
