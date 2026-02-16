# Fitness Tracker - Backend

Python/FastAPI Backend für die Fitness Tracker Anwendung.

## Setup

### 1. Virtual Environment erstellen
```bash
python -m venv venv
```

### 2. Virtual Environment aktivieren
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Dependencies installieren
```bash
pip install -r requirements.txt
```

### 4. Umgebungsvariablen konfigurieren
```bash
cp .env.example .env
# Dann .env editieren und Datenbank-Zugangsdaten eintragen
```

### 5. Server starten
```bash
uvicorn app.main:app --reload
```

API läuft dann auf: http://localhost:8000

## API Dokumentation

FastAPI generiert automatisch eine interaktive API-Dokumentation:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Projekt-Struktur

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # Haupt-App
│   ├── models/           # Datenbank-Modelle
│   ├── routes/           # API-Endpoints
│   ├── schemas/          # Pydantic-Schemas
│   └── database.py       # DB-Konfiguration
├── alembic/              # Datenbank-Migrationen
├── venv/                 # Virtual Environment (nicht in Git)
├── .env                  # Umgebungsvariablen (nicht in Git)
├── .env.example          # Template
└── requirements.txt      # Python-Dependencies
```

## Technologien

- **FastAPI** - Web Framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Datenbank
- **Alembic** - Migrations
- **Pydantic** - Validierung
