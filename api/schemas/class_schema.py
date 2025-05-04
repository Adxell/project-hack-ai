import uuid
from typing import List, Any, Dict
from pydantic import EmailStr, BaseModel, Field
from enum import Enum


class Class_usuario_schema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    id_professor: uuid.UUID 

    class Config:
        orm_mode = True


class CreateClass_schema(BaseModel):
    """Esquema para la creación de usuario solo con email."""
    name: str

    class Config:
        orm_mode = True



class EnrollClass_schema(BaseModel):
    """Esquema para la creación de usuario solo con email."""
    id: uuid.UUID

    class Config:
        orm_mode = True
