"""
FastAPI Dependencies
- get_db: Datenbank-Session
- get_current_user: Aktuell eingeloggter User
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.security import decode_access_token

# OAuth2-Schema für Bearer-Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency: Gibt den aktuell eingeloggten User zurück

    Validiert den JWT-Token und lädt den User aus der Datenbank.
    Wirft eine HTTPException wenn Token ungültig oder User nicht gefunden.

    Args:
        token: JWT-Token aus dem Authorization-Header
        db: Datenbank-Session

    Returns:
        User-Objekt des eingeloggten Users

    Raises:
        HTTPException: 401 wenn Token ungültig oder User nicht gefunden
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Token dekodieren
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # Username aus Token extrahieren
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    # User aus Datenbank laden
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    # User muss aktiv sein
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user


def get_current_active_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency: Gibt den aktuellen User zurück, nur wenn Admin

    Args:
        current_user: Aktueller User (automatisch injiziert)

    Returns:
        User-Objekt wenn Admin

    Raises:
        HTTPException: 403 wenn User kein Admin ist
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
