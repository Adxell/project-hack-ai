import io
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
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
#sqlalchemy 
from sqlalchemy.orm import Session
#verify 
from security.security import get_current_user
#db
from db_config.database import get_db
#schema
from ..schemas.class_schema import CreateClass_schema, EnrollClass_schema
#models
from ..models.course_model import Course, CourseStudens
router = APIRouter()


@router.post('/create_class_room', summary="Create class room") 
async def create(request: Request, 
                 payload: CreateClass_schema,
                 db: Session = Depends(get_db),
                 data_login: Dict[str, Any] = Depends(get_current_user)):
    try:

        new_course = Course(course_name=payload.name, 
                            professor_id = data_login.get('id'))
        
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        
        return JSONResponse(content=jsonable_encoder({"status": status.HTTP_201_CREATED, 
                                                      "data": new_course, 
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


@router.get('/get_course_by_professor/{id_professor}', summary="Get course by professor") 
async def get(request: Request, 
                 id_professor: UUID,
                 db: Session = Depends(get_db),
                 data_login: Dict[str, Any] = Depends(get_current_user)):
    try:
        if data_login.get('role') != 'profesor': 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No tiene permiso para ver este apartado")
        courses = db.query(Course).filter(Course.professor_id == id_professor).all()
        if len(courses) == 0: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Cursos Encontrado")
        return JSONResponse(content=jsonable_encoder({"status": status.HTTP_200_OK, 
                                                      "data": courses, 
                                                      "success": True}), 
                                                      status_code=status.HTTP_200_OK) 
    except HTTPException as httpe: 
        return JSONResponse(content=jsonable_encoder({"status": httpe.status_code,  
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


@router.get('/get_all_courses', summary="Get all course") 
async def get(request: Request, 
            db: Session = Depends(get_db),
            data_login: Dict[str, Any] = Depends(get_current_user)):
    try:
        
        courses = db.query(Course).all()
        
        return JSONResponse(content=jsonable_encoder({"status": status.HTTP_200_OK, 
                                                      "data": courses, 
                                                      "success": True}), 
                                                      status_code=status.HTTP_200_OK) 
    except HTTPException as httpe: 
        return JSONResponse(content=jsonable_encoder({"status": httpe.status_code,  
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

@router.get('/get_courses_by_student/{id_student}', summary="Get courses by student") 
async def get(request: Request, 
            id_student: str, 
            db: Session = Depends(get_db),
            data_login: Dict[str, Any] = Depends(get_current_user)):
    try:
        
        courses_id = db.query(CourseStudens).filter(CourseStudens.student_id == id_student).all()
        
        if len(courses_id) > 0: 
            courses = [db.query(Course).filter(Course.id == i.course_id).first() for i in courses_id]
            
        return JSONResponse(content=jsonable_encoder({"status": status.HTTP_200_OK, 
                                                      "data": courses, 
                                                      "success": True}), 
                                                      status_code=status.HTTP_200_OK) 
    except HTTPException as httpe: 
        return JSONResponse(content=jsonable_encoder({"status": httpe.status_code,  
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


@router.post('/enrolle_class', summary="Inscribir class") 
async def post(request: Request, 
                payload: EnrollClass_schema,
                db: Session = Depends(get_db),
                data_login: Dict[str, Any] = Depends(get_current_user)):
    try:
        if data_login.get('role') == 'profesor': 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No tiene permiso para hacer esta accion")
        
        existe_registro = db.query(CourseStudens).filter(CourseStudens.course_id == payload.id, 
                                       CourseStudens.student_id == data_login.get('id')).first()

        if existe_registro: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya se encuentra registo a la clase")
        

        new_enrolle = CourseStudens(course_id = payload.id, 
                                    student_id = data_login.get('id'))
        
        db.add(new_enrolle)
        db.commit()
        db.refresh(new_enrolle)
        return JSONResponse(content=jsonable_encoder({"status": status.HTTP_201_CREATED, 
                                                      "data": new_enrolle, 
                                                      "success": True}), 
                                                      status_code=status.HTTP_201_CREATED) 
    except HTTPException as httpe: 
        return JSONResponse(content=jsonable_encoder({"status": httpe.status_code,  
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
