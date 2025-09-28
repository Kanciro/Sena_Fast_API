from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserProfileCreate(BaseModel):
    nombre_completo: str = Field(..., example="Jhon Deivy Medina Vargas")
    telefono: str = Field(..., example="300-1234567")
    direccion: str = Field(..., example="Calle Falsa 123")

class UserProfileOut(UserProfileCreate):
    id: int
    user_id: int

class UserAssignmentCreate(BaseModel):
    user_id: int
    service_id: int = Field(..., example=123)
    description: str = Field(..., example="Asignación de servicio de masajes")

class UserAssignmentOut(UserAssignmentCreate):
    id: int
    is_active: bool
    start_date: datetime