"""
Training Models - Trainingstage und Übungen
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Training(Base):
    """
    Training - Ein Trainingstag

    Beispiel: "Brust/Bizeps Training am 16.02.2026"
    Enthält mehrere Exercises (Übungen)
    """
    __tablename__ = "trainings"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Training-Info
    date = Column(Date, nullable=False, index=True)
    title = Column(String(200), nullable=True)  # z.B. "Brust/Bizeps", "Leg Day"
    notes = Column(Text, nullable=True)  # Notizen zum Training
    duration_minutes = Column(Integer, nullable=True)  # Trainingsdauer

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="trainings")
    exercises = relationship("Exercise", back_populates="training", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Training(id={self.id}, user_id={self.user_id}, date={self.date}, title='{self.title}')>"


class Exercise(Base):
    """
    Exercise - Eine Übung innerhalb eines Trainings

    Beispiel: "Bankdrücken: 3 Sätze x 10 Wiederholungen @ 80kg"
    """
    __tablename__ = "exercises"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    training_id = Column(Integer, ForeignKey("trainings.id", ondelete="CASCADE"), nullable=False, index=True)

    # Übungs-Details
    name = Column(String(200), nullable=False)  # z.B. "Bankdrücken", "Kniebeugen"
    sets = Column(Integer, nullable=True)  # Anzahl Sätze
    reps = Column(Integer, nullable=True)  # Wiederholungen pro Satz
    weight = Column(Float, nullable=True)  # Gewicht in kg
    notes = Column(Text, nullable=True)  # Notizen zur Übung

    # Reihenfolge in der Übungsliste
    order = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    training = relationship("Training", back_populates="exercises")

    def __repr__(self):
        return f"<Exercise(id={self.id}, name='{self.name}', sets={self.sets}x{self.reps} @ {self.weight}kg)>"
