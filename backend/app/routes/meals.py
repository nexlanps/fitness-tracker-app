"""
Meal Routes - CRUD Operations
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.models.user import User
from app.models.meal import Meal
from app.schemas.meal import (
    Meal as MealSchema,
    MealCreate,
    MealUpdate
)
from app.core.deps import get_current_user

router = APIRouter(prefix="/meals", tags=["Meals"])


@router.get("/", response_model=List[MealSchema])
def list_meals(
    user_id: Optional[int] = Query(None, description="Filter by user_id"),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listet Meals auf"""
    query = db.query(Meal)

    if user_id is not None:
        query = query.filter(Meal.user_id == user_id)
    else:
        query = query.filter(Meal.user_id == current_user.id)

    if start_date:
        query = query.filter(Meal.date >= start_date)
    if end_date:
        query = query.filter(Meal.date <= end_date)

    meals = query.order_by(Meal.date.desc()).all()
    return meals


@router.get("/{meal_id}", response_model=MealSchema)
def get_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Gibt eine spezifische Meal zurück"""
    meal = db.query(Meal).filter(Meal.id == meal_id).first()

    if not meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found"
        )

    return meal


@router.post("/", response_model=MealSchema, status_code=status.HTTP_201_CREATED)
def create_meal(
    meal_data: MealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Erstellt eine neue Meal"""
    new_meal = Meal(
        user_id=current_user.id,
        **meal_data.model_dump()
    )

    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)

    return new_meal


@router.put("/{meal_id}", response_model=MealSchema)
def update_meal(
    meal_id: int,
    meal_data: MealUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Aktualisiert eine Meal (nur eigene!)"""
    meal = db.query(Meal).filter(Meal.id == meal_id).first()

    if not meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found"
        )

    if meal.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to edit this meal"
        )

    update_data = meal_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(meal, field, value)

    db.commit()
    db.refresh(meal)

    return meal


@router.delete("/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Löscht eine Meal (nur eigene!)"""
    meal = db.query(Meal).filter(Meal.id == meal_id).first()

    if not meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found"
        )

    if meal.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this meal"
        )

    db.delete(meal)
    db.commit()

    return None
