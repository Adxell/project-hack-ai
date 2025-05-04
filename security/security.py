from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from pydantic import BaseModel
from setup.config import settings
from fastapi import status , HTTPException, Header
from uuid import UUID


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

class TokenData(BaseModel):
    """Esquema para los datos contenidos dentro del token JWT."""
    email: Optional[str] = None
    id: UUID
    role: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Genera un nuevo token de acceso JWT.

    Args:
        data (dict): Datos para codificar en el token (payload).
                     Debe contener la clave 'sub' (subject/identificador).
        expires_delta (Optional[timedelta]): Tiempo de expiración personalizado.
                                              Si es None, usa el default de config.

    Returns:
        str: El token JWT codificado como string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verifica un token JWT y extrae el payload."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("email")
    id: UUID = payload.get("id")
    role: str = payload.get("role")

    token_data = TokenData(email=email, 
                           id=id, 
                           role=role)
    return token_data

async def get_current_user(Authorization: str = Header(...)):
    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Encabezado de autorización inválido o faltante")
    token = Authorization.split(" ")[1]
    user_data = verify_token(token)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    return {**user_data.model_dump()}
