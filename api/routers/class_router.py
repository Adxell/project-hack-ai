import io
from typing import Optional, Dict, Any
from datetime import datetime
# import pytz
#sqlalchemy
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import DatabaseError
#fastapi
from fastapi import APIRouter, File, UploadFile, Form, Request, status , HTTPException, Depends, Header
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
#security
from agents.generator_agent import generar_examen_ia_json_multiple
#verify 
from security.security import get_current_user
#schema
from ..schemas.class_schema import CreateClass_schema
router = APIRouter()


@router.post('/create_class_room', summary="Create class room") 
async def create(request: Request, 
                 payload: CreateClass_schema,
                 data_login: Dict[str, Any] = Depends(get_current_user)):
    try:
        print(payload)
        print(data_login)
        return JSONResponse(content=jsonable_encoder({"status": status.HTTP_201_CREATED, 
                                                      "data": "ok", 
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
