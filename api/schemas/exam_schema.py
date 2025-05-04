import uuid
from typing import List, Any, Dict
from pydantic import BaseModel, Field

class Exam_schema(BaseModel):
    """
    Modelo Pydantic para representar la tabla Examenes.
    Utiliza UUID para el campo id y para la clave foránea profesor_id.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    tema: str
    preguntas: List[Any] | Dict[str, Any]
    profesor_id: uuid.UUID

    class Config:
        orm_mode = True



class CreateExam_schema(BaseModel):
    """
    Modelo Pydantic para representar la tabla Examenes.
    Utiliza UUID para el campo id y para la clave foránea profesor_id.
    """
    input: str
    docs: List[Any] | Dict[str, Any]

    class Config:
        orm_mode = True


class Options(BaseModel): 
    opcion_letra: str 
    opcion_texto: str

class Question(BaseModel): 
    numero: int
    tipo: str
    pregunta_texto: str
    opciones: list[Options]
    respuesta_correcta_letra: str

class SaveExam_schema(BaseModel):
    examen: list[Question]
    tema: str

