import uuid
from typing import List, Any, Dict
from pydantic import EmailStr, BaseModel, Field
from enum import Enum

class RolUsuario(str, Enum):
    """Enumera los roles posibles para un usuario."""
    ESTUDIANTE = 'estudiante'
    PROFESOR = 'profesor'

class User_Schema(BaseModel):
    """
    Modelo Pydantic para representar la tabla Usuarios.
    Utiliza UUID para el campo id.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    role: RolUsuario

    class Config:
        orm_mode = True
        use_enum_values = True


class UserCreateByEmail(BaseModel):
    """Esquema para la creación de usuario solo con email."""
    email: EmailStr
    role: RolUsuario
    class Config:
        orm_mode = True
        use_enum_values = True



class UserLoginByEmail(BaseModel):
    email: EmailStr
    class Config:
        orm_mode = True

