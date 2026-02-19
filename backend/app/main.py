"""
Fitness Tracker API - Main Application
FastAPI Backend für Fitness-Tracking mit Kalender und Messdaten
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# .env Datei laden
load_dotenv()

# Router importieren
from app.routes import auth, users, trainings, measurements, meals

# App-Instanz erstellen
app = FastAPI(
    title="Fitness Tracker API",
    description="Backend für Fitness-Tracking App mit Training, Messungen und Ernährung",
    version="0.2.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS aktivieren (damit Frontend kommunizieren kann)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Production einschränken!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router registrieren
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(trainings.router, prefix="/api")
app.include_router(measurements.router, prefix="/api")
app.include_router(meals.router, prefix="/api")

# Root-Endpoint (Test)
@app.get("/")
def read_root():
    """
    Basis-Endpoint zum Testen der API
    """
    return {
        "message": "Fitness Tracker API läuft!",
        "version": "0.2.0",
        "status": "ok",
        "docs": "/api/docs"
    }

# Health-Check Endpoint
@app.get("/health")
def health_check():
    """
    Health-Check für Monitoring
    """
    return {"status": "healthy"}
