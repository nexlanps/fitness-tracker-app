"""
Meal Model - Hauptmahlzeiten
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class MealType(str, enum.Enum):
    """
    Enum für Mahlzeit-Typen
    """
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class Meal(Base):
    """
    Meal - Hauptmahlzeit an einem bestimmten Tag

    Wird im Kalender angezeigt zusammen mit Trainings und Messungen
    """
    __tablename__ = "meals"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Mahlzeit-Info
    date = Column(Date, nullable=False, index=True)
    meal_type = Column(Enum(MealType), nullable=False)  # Frühstück/Mittag/Abend/Snack

    # Details
    title = Column(String(200), nullable=True)  # z.B. "Hähnchen mit Reis"
    description = Column(Text, nullable=True)  # Detaillierte Beschreibung

    # Nährwerte (optional)
    calories = Column(Integer, nullable=True)  # Kalorien
    protein = Column(Float, nullable=True)  # Protein in g
    carbs = Column(Float, nullable=True)  # Kohlenhydrate in g
    fat = Column(Float, nullable=True)  # Fett in g

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="meals")

    def __repr__(self):
        return f"<Meal(id={self.id}, user_id={self.user_id}, date={self.date}, type={self.meal_type}, title='{self.title}')>"
