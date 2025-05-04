import io
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
# import pytz
#sqlalchemy
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import DatabaseError
#fastapi
from fastapi import APIRouter, File, UploadFile, Form, Request, status , HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
#sqlachemy 
from sqlalchemy.orm import Session
#security
from security.security import get_current_user
#schemas
from ..schemas.exam_schema import SaveAnswers_schema
#models
from ..models.exam_model import ExamResult
#db
from db_config.database import get_db

router = APIRouter()


@router.post('/guardar_respuestas', summary="Guardar respuesta") 
async def create(request: Request, 
                 payload: SaveAnswers_schema,
                 db: Session = Depends(get_db),
                 data_login: Dict[str, Any] = Depends(get_current_user)):
    try:
        id_user = data_login.get('id')
        answers = [i.model_dump() for i in payload.answers]
        
        new_examen_result = ExamResult(exam_id = payload.exam_id, 
                                       student_id = payload.student_id, 
                                       score = payload.score, 
                                       answers = answers)
        
        db.add(new_examen_result)
        db.commit()

        db.refresh(new_examen_result)

        return JSONResponse(content=jsonable_encoder({"status": status.HTTP_201_CREATED, 
                                                      "data": new_examen_result, 
                                                      "success": True}), 
                                                      status_code=status.HTTP_201_CREATED) 
    except HTTPException as httpe: 
        return JSONResponse(content=jsonable_encoder({"status": status.HTTP_400_BAD_REQUEST,  
                                                      "message": httpe.detail, 
                                                      "success": False, 
                                                      "time": datetime.now(), 
                                                      "path": request.url.path}), 
                                                      status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                                      "message": "Error Interno", 
                                                      "error": str(e.args), 
                                                      "success": False, 
                                                      "time": datetime.now(), 
                                                      "path": request.url.path}), 
                                                      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
