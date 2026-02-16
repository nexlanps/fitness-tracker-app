"""
Fitness Tracker API - Main Application
FastAPI Backend für Fitness-Tracking mit Kalender und Messdaten
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# App-Instanz erstellen
app = FastAPI(
    title="Fitness Tracker API",
    description="Backend für Fitness-Tracking App mit Training, Messungen und Ernährung",
    version="0.1.0"
)

# CORS aktivieren (damit Frontend kommunizieren kann)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Production einschränken!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root-Endpoint (Test)
@app.get("/")
def read_root():
    """
    Basis-Endpoint zum Testen der API
    """
    return {
        "message": "Fitness Tracker API läuft!",
        "version": "0.1.0",
        "status": "ok"
    }

# Health-Check Endpoint
@app.get("/health")
def health_check():
    """
    Health-Check für Monitoring
    """
    return {"status": "healthy"}
