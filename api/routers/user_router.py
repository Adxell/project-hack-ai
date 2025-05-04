from datetime import datetime
# import pytz
#sqlalchemy
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import DatabaseError
#fastapi
from fastapi import APIRouter, Request, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
#sqlachemy 
from sqlalchemy.orm import Session
#Schemas
from ..schemas.user_schema import  UserCreateByEmail,UserLoginByEmail
#security
from security.security import create_access_token
#models
from ..models.user_model import User
#db 
from db_config.database import get_db
router = APIRouter()

@router.post('/create_user', summary="Insert User") 
async def create(request: Request, 
                 payload: UserCreateByEmail, 
                 db: Session = Depends(get_db)):
    try:

        old_user = db.query(User.email).filter(User.email == payload.email).first()

        if old_user: 
            raise HTTPException(400, "Usuario ya registrado")
        
        user_data = User(**payload.model_dump())
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        token = create_access_token({"id": str(user_data.id),
                                     "email": user_data.email,
                                     "role": user_data.role })
        
        return JSONResponse(content=jsonable_encoder({"status": status.HTTP_201_CREATED, 
                                                      "data": {
                                                          "token": token, 
                                                          "email": user_data.email, 
                                                          "role": user_data.role
                                                      }, 
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


@router.post('/login_user', summary="Login User") 
async def post(request: Request, 
                 payload: UserLoginByEmail, 
                 db: Session = Depends(get_db)):
    try:

        old_user = db.query(User).filter(User.email == payload.email).first()

        if not old_user: 
            raise HTTPException(404, "Usuario no se encuentra registrado registrado")
        
        token = create_access_token({"id": str(old_user.id),
                                     "email": old_user.email,
                                     "role": old_user.role })
        
        return JSONResponse(content=jsonable_encoder({"status": status.HTTP_201_CREATED, 
                                                      "data": {
                                                          "token": token, 
                                                          "email": old_user.email, 
                                                          "role": old_user.role
                                                      }, 
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
    