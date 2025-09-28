from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    assignments = relationship("UserAssignment", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    nombre_completo = Column(String)
    telefono = Column(String)
    direccion = Column(String)
    user = relationship("User", back_populates="profile")

class UserAssignment(Base):
    __tablename__ = "user_assignments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, index=True)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="assignments")