"""
Authentication Routes
- Login
- Register (nur für Admin)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, User as UserSchema
from app.core.security import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.deps import get_current_active_admin

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login-Endpoint

    Validiert Username & Passwort und gibt JWT-Token zurück.

    Args:
        form_data: OAuth2-Formular (username, password)
        db: Datenbank-Session

    Returns:
        JWT-Access-Token

    Raises:
        HTTPException 401: Wenn Credentials falsch
    """
    # User aus Datenbank laden
    user = db.query(User).filter(User.username == form_data.username).first()

    # User existiert nicht oder Passwort falsch
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # User ist deaktiviert
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    # JWT-Token erstellen
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_admin)
):
    """
    Registrierungs-Endpoint (nur für Admin!)

    Erstellt einen neuen User. Nur Admins können User erstellen.

    Args:
        user_data: User-Daten (username, name, password)
        db: Datenbank-Session
        current_admin: Aktueller Admin-User (Dependency)

    Returns:
        Erstellter User

    Raises:
        HTTPException 400: Wenn Username bereits existiert
        HTTPException 403: Wenn kein Admin
    """
    # Prüfen ob Username bereits existiert
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Passwort hashen
    hashed_password = get_password_hash(user_data.password)

    # User erstellen
    new_user = User(
        username=user_data.username,
        name=user_data.name,
        password_hash=hashed_password,
        is_active=True,
        is_admin=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
