"""
Measurement Schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime


class MeasurementBase(BaseModel):
    """Basis-Felder für Measurement"""
    date: date
    weight: Optional[float] = Field(None, ge=0, le=500)  # kg
    body_fat: Optional[float] = Field(None, ge=0, le=100)  # %
    waist: Optional[float] = Field(None, ge=0, le=300)  # cm
    bmi: Optional[float] = Field(None, ge=0, le=100)
    chest: Optional[float] = Field(None, ge=0, le=300)  # cm
    hips: Optional[float] = Field(None, ge=0, le=300)  # cm
    thigh: Optional[float] = Field(None, ge=0, le=300)  # cm
    arm: Optional[float] = Field(None, ge=0, le=100)  # cm
    notes: Optional[str] = None


class MeasurementCreate(MeasurementBase):
    """Schema für Measurement-Erstellung"""
    pass


class MeasurementUpdate(BaseModel):
    """Schema für Measurement-Update"""
    date: Optional[date] = None
    weight: Optional[float] = Field(None, ge=0, le=500)
    body_fat: Optional[float] = Field(None, ge=0, le=100)
    waist: Optional[float] = Field(None, ge=0, le=300)
    bmi: Optional[float] = Field(None, ge=0, le=100)
    chest: Optional[float] = Field(None, ge=0, le=300)
    hips: Optional[float] = Field(None, ge=0, le=300)
    thigh: Optional[float] = Field(None, ge=0, le=300)
    arm: Optional[float] = Field(None, ge=0, le=100)
    notes: Optional[str] = None


class Measurement(MeasurementBase):
    """Schema für Measurement-Response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
