"""
Measurement Model - Körpermessungen
"""
from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Measurement(Base):
    """
    Measurement - Körpermessung an einem bestimmten Tag

    Enthält: Gewicht, Körperfett, Bauchumfang, BMI
    """
    __tablename__ = "measurements"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Messdatum
    date = Column(Date, nullable=False, index=True)

    # Messwerte
    weight = Column(Float, nullable=True)  # Gewicht in kg
    body_fat = Column(Float, nullable=True)  # Körperfett in %
    waist = Column(Float, nullable=True)  # Bauchumfang in cm
    bmi = Column(Float, nullable=True)  # Body Mass Index

    # Optional: Weitere Messwerte
    chest = Column(Float, nullable=True)  # Brustumfang in cm
    hips = Column(Float, nullable=True)  # Hüftumfang in cm
    thigh = Column(Float, nullable=True)  # Oberschenkelumfang in cm
    arm = Column(Float, nullable=True)  # Armumfang in cm

    # Notizen
    notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="measurements")

    def __repr__(self):
        return f"<Measurement(id={self.id}, user_id={self.user_id}, date={self.date}, weight={self.weight}kg)>"
