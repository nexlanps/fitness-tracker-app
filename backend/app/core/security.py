"""
Security-Funktionen für Authentifizierung
- Password-Hashing (bcrypt)
- JWT-Token-Erstellung und -Validierung
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
import os

# JWT-Konfiguration aus Umgebungsvariablen
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-CHANGE-IN-PRODUCTION")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Überprüft, ob das eingegebene Passwort mit dem Hash übereinstimmt

    Args:
        plain_password: Klartext-Passwort vom User
        hashed_password: Gehashtes Passwort aus der Datenbank

    Returns:
        True wenn Passwort korrekt, sonst False
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def get_password_hash(password: str) -> str:
    """
    Hasht ein Passwort mit bcrypt

    Args:
        password: Klartext-Passwort

    Returns:
        Gehashtes Passwort
    """
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Erstellt einen JWT-Access-Token

    Args:
        data: Payload-Daten (z.B. {"sub": "username"})
        expires_delta: Optionale Gültigkeitsdauer

    Returns:
        JWT-Token als String
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Dekodiert und validiert einen JWT-Token

    Args:
        token: JWT-Token

    Returns:
        Payload-Daten wenn gültig, sonst None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
