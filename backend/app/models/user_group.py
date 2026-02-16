"""
UserGroup Models - Gruppen für gemeinsame Dateneinsicht
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class UserGroup(Base):
    """
    UserGroup - Gruppe von Usern die gegenseitig Daten sehen können

    Beispiel: "Fitness-Buddies", "Familie Schmidt", "Gym-Crew"
    """
    __tablename__ = "user_groups"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Gruppen-Info
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    # Gruppe hat viele Mitglieder (über UserGroupMembership)
    memberships = relationship("UserGroupMembership", back_populates="group", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<UserGroup(id={self.id}, name='{self.name}')>"


class UserGroupMembership(Base):
    """
    UserGroupMembership - Verbindung zwischen User und UserGroup

    Many-to-Many Relationship: Ein User kann in mehreren Gruppen sein,
    eine Gruppe kann mehrere User haben.
    """
    __tablename__ = "user_group_memberships"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    group_id = Column(Integer, ForeignKey("user_groups.id", ondelete="CASCADE"), nullable=False)

    # Timestamps
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="group_memberships")
    group = relationship("UserGroup", back_populates="memberships")

    def __repr__(self):
        return f"<UserGroupMembership(user_id={self.user_id}, group_id={self.group_id})>"
