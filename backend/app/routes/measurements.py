"""
Measurement Routes - CRUD Operations
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.models.user import User
from app.models.measurement import Measurement
from app.schemas.measurement import (
    Measurement as MeasurementSchema,
    MeasurementCreate,
    MeasurementUpdate
)
from app.core.deps import get_current_user

router = APIRouter(prefix="/measurements", tags=["Measurements"])


@router.get("/", response_model=List[MeasurementSchema])
def list_measurements(
    user_id: Optional[int] = Query(None, description="Filter by user_id"),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listet Measurements auf"""
    query = db.query(Measurement)

    if user_id is not None:
        query = query.filter(Measurement.user_id == user_id)
    else:
        query = query.filter(Measurement.user_id == current_user.id)

    if start_date:
        query = query.filter(Measurement.date >= start_date)
    if end_date:
        query = query.filter(Measurement.date <= end_date)

    measurements = query.order_by(Measurement.date.desc()).all()
    return measurements


@router.get("/{measurement_id}", response_model=MeasurementSchema)
def get_measurement(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Gibt eine spezifische Measurement zurück"""
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()

    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found"
        )

    return measurement


@router.post("/", response_model=MeasurementSchema, status_code=status.HTTP_201_CREATED)
def create_measurement(
    measurement_data: MeasurementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Erstellt eine neue Measurement"""
    new_measurement = Measurement(
        user_id=current_user.id,
        **measurement_data.model_dump()
    )

    db.add(new_measurement)
    db.commit()
    db.refresh(new_measurement)

    return new_measurement


@router.put("/{measurement_id}", response_model=MeasurementSchema)
def update_measurement(
    measurement_id: int,
    measurement_data: MeasurementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Aktualisiert eine Measurement (nur eigene!)"""
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()

    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found"
        )

    if measurement.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to edit this measurement"
        )

    update_data = measurement_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(measurement, field, value)

    db.commit()
    db.refresh(measurement)

    return measurement


@router.delete("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_measurement(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Löscht eine Measurement (nur eigene!)"""
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()

    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found"
        )

    if measurement.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this measurement"
        )

    db.delete(measurement)
    db.commit()

    return None
