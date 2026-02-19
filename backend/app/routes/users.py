"""
User Routes
- Get current user
- List users (für User-Auswahl)
- Get user by ID
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserInList
from app.core.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserSchema)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Gibt Informationen über den aktuell eingeloggten User zurück

    Args:
        current_user: Aktueller User (automatisch injiziert)

    Returns:
        User-Objekt
    """
    return current_user


@router.get("/", response_model=List[UserInList])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Listet alle aktiven User auf

    Für die User-Auswahl im Frontend (Dropdown).
    User sieht sich selbst + alle User in seinen Gruppen.

    Args:
        db: Datenbank-Session
        current_user: Aktueller User

    Returns:
        Liste von Usern
    """
    # TODO: Später filtern nach Gruppen-Zugehörigkeit
    # Aktuell: Alle aktiven User
    users = db.query(User).filter(User.is_active == True).all()
    return users


@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Gibt User-Details zurück

    Args:
        user_id: ID des Users
        db: Datenbank-Session
        current_user: Aktueller User

    Returns:
        User-Objekt

    Raises:
        HTTPException 404: Wenn User nicht gefunden
        HTTPException 403: Wenn keine Berechtigung
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # TODO: Prüfen ob current_user Berechtigung hat, diesen User zu sehen
    # (gleiche Gruppe oder sich selbst)

    return user
