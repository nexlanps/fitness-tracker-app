"""
Training Routes - CRUD Operations
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.models.user import User
from app.models.training import Training, Exercise
from app.schemas.training import (
    Training as TrainingSchema,
    TrainingCreate,
    TrainingUpdate,
    TrainingInList
)
from app.core.deps import get_current_user

router = APIRouter(prefix="/trainings", tags=["Trainings"])


@router.get("/", response_model=List[TrainingInList])
def list_trainings(
    user_id: Optional[int] = Query(None, description="Filter by user_id"),
    start_date: Optional[date] = Query(None, description="Filter von Datum"),
    end_date: Optional[date] = Query(None, description="Filter bis Datum"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Listet Trainings auf mit optionalen Filtern

    Args:
        user_id: Optional - filtert nach User
        start_date: Optional - filtert Trainings ab diesem Datum
        end_date: Optional - filtert Trainings bis zu diesem Datum
        db: Datenbank-Session
        current_user: Aktueller User

    Returns:
        Liste von Trainings
    """
    query = db.query(Training)

    # Filter nach user_id (wenn nicht angegeben: aktueller User)
    if user_id is not None:
        query = query.filter(Training.user_id == user_id)
    else:
        query = query.filter(Training.user_id == current_user.id)

    # Filter nach Datum
    if start_date:
        query = query.filter(Training.date >= start_date)
    if end_date:
        query = query.filter(Training.date <= end_date)

    # Sortierung: Neueste zuerst
    trainings = query.order_by(Training.date.desc()).all()
    return trainings


@router.get("/{training_id}", response_model=TrainingSchema)
def get_training(
    training_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Gibt ein spezifisches Training mit allen Exercises zurück

    Args:
        training_id: ID des Trainings
        db: Datenbank-Session
        current_user: Aktueller User

    Returns:
        Training mit Exercises

    Raises:
        HTTPException 404: Wenn Training nicht gefunden
    """
    training = db.query(Training).filter(Training.id == training_id).first()

    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found"
        )

    # TODO: Permission-Check (Gruppen-Mitgliedschaft)

    return training


@router.post("/", response_model=TrainingSchema, status_code=status.HTTP_201_CREATED)
def create_training(
    training_data: TrainingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Erstellt ein neues Training mit Exercises

    Args:
        training_data: Training-Daten
        db: Datenbank-Session
        current_user: Aktueller User

    Returns:
        Erstelltes Training
    """
    # Training erstellen
    new_training = Training(
        user_id=current_user.id,
        date=training_data.date,
        title=training_data.title,
        notes=training_data.notes,
        duration_minutes=training_data.duration_minutes
    )

    db.add(new_training)
    db.flush()  # Generiert ID für new_training

    # Exercises hinzufügen
    for exercise_data in training_data.exercises:
        exercise = Exercise(
            training_id=new_training.id,
            **exercise_data.model_dump()
        )
        db.add(exercise)

    db.commit()
    db.refresh(new_training)

    return new_training


@router.put("/{training_id}", response_model=TrainingSchema)
def update_training(
    training_id: int,
    training_data: TrainingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Aktualisiert ein Training (nur eigene Trainings!)

    Args:
        training_id: ID des Trainings
        training_data: Neue Daten
        db: Datenbank-Session
        current_user: Aktueller User

    Returns:
        Aktualisiertes Training

    Raises:
        HTTPException 404: Wenn Training nicht gefunden
        HTTPException 403: Wenn nicht eigenes Training
    """
    training = db.query(Training).filter(Training.id == training_id).first()

    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found"
        )

    # Nur eigene Trainings bearbeiten
    if training.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to edit this training"
        )

    # Update-Felder
    update_data = training_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(training, field, value)

    db.commit()
    db.refresh(training)

    return training


@router.delete("/{training_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_training(
    training_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Löscht ein Training (nur eigene Trainings!)

    Args:
        training_id: ID des Trainings
        db: Datenbank-Session
        current_user: Aktueller User

    Raises:
        HTTPException 404: Wenn Training nicht gefunden
        HTTPException 403: Wenn nicht eigenes Training
    """
    training = db.query(Training).filter(Training.id == training_id).first()

    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training not found"
        )

    # Nur eigene Trainings löschen
    if training.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this training"
        )

    db.delete(training)
    db.commit()

    return None
