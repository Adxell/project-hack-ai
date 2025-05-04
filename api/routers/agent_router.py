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
#agents
from agents.generator_agent import generar_examen_ia_json_multiple
#security
from security.security import get_current_user
#schemas
from ..schemas.exam_schema import SaveExam_schema
#models
from ..models.exam_model import Exam
#db
from db_config.database import get_db

router = APIRouter()


@router.post('/create_examen', summary="Create examen") 
async def create(request: Request, 
                 text_data: str = Form(...),
                 file: Optional[UploadFile] = File(None), 
                 data_login: Dict[str, Any] = Depends(get_current_user)):
    try:
        result_test = generar_examen_ia_json_multiple(text_data, await file.read() if file else None)

        return JSONResponse(content=jsonable_encoder({"status": status.HTTP_201_CREATED, 
                                                      "data": result_test, 
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




@router.post('/guardar_examen', summary="Create examen") 
async def create(request: Request, 
                 payload: SaveExam_schema,
                 db: Session = Depends(get_db),
                 data_login: Dict[str, Any] = Depends(get_current_user)):
    try:
        id_user = data_login.get('id')
        questions = [i.model_dump() for i in payload.examen]
        new_exam = Exam(topic = payload.tema, 
                    questions = questions,
                    professor_id = id_user)
        db.add(new_exam)
        db.commit()

        db.refresh(new_exam)

        return JSONResponse(content=jsonable_encoder({"status": status.HTTP_201_CREATED, 
                                                      "data": new_exam, 
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
