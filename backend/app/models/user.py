"""
User Model - Benutzer mit Authentifizierung
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    User-Tabelle für Authentifizierung und Profile

    Jeder User hat eigene Daten (Training/Measurement/Meal).
    User können in Gruppen sein und gegenseitig Daten sehen.
    """
    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Authentifizierung
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # Profil
    name = Column(String(100), nullable=False)  # Display Name

    # Status
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    # User hat viele Trainings
    trainings = relationship("Training", back_populates="user", cascade="all, delete-orphan")

    # User hat viele Measurements
    measurements = relationship("Measurement", back_populates="user", cascade="all, delete-orphan")

    # User hat viele Meals
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")

    # User ist in vielen Gruppen (über UserGroupMembership)
    group_memberships = relationship("UserGroupMembership", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', name='{self.name}')>"
