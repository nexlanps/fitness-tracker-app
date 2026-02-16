"""
Datenbank-Konfiguration und Session-Management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# .env Datei laden
load_dotenv()

# Datenbank-URL aus Umgebungsvariablen
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy Engine erstellen
# echo=True zeigt SQL-Queries in der Console (für Development)
engine = create_engine(
    DATABASE_URL,
    echo=True,  # In Production auf False setzen
    pool_pre_ping=True,  # Prüft Verbindung vor Nutzung
)

# Session-Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base-Klasse für alle Models
Base = declarative_base()


# Dependency für FastAPI
def get_db():
    """
    Erstellt eine Datenbank-Session für jeden Request.
    Wird automatisch geschlossen nach dem Request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
