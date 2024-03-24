from fastapi import (
    APIRouter, BackgroundTasks, Depends, status)
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from src.auth import auth_service, jwt, schemas, security
from src.config import settings
from sqlalchemy.orm import Session
from src.database import get_db
from src.user import crud
from src.auth.mail import forget_pwd_email, verify_email
from src.exceptions import (
    NotFound, 
    InvalidToken, 
    InvalidPassword, 
    InvalidVerify
)


router = APIRouter()


@router.post("/verify", 
            summary="Verify user email", 
            response_model=schemas.VerifyUserSchema, 
            dependencies=[Depends(jwt.get_current_user_from_token)])
async def verify(
    background_tasks: BackgroundTasks, 
    data: schemas.VerifyUserSchema, 
    db: Session= Depends(get_db)):        
    
    user = crud.get_user_by_login(db, login=data.email)
    if not user:
        raise InvalidVerify()
    
    token = jwt.create_activate_token(data={"sub": user.email})
    activate_link =  f"https://{settings.FRONT_HOST}/activate/{token}"
    message = verify_email(link=activate_link, user=user)
    
    template_name = "mail/user_activate.html"        
    background_tasks.add_task(settings.fastmail.send_message, message, template_name)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'success': True,
            "message": "Email has been sent"
        }
    )    


@router.post("/activate", 
             summary="Activate new user", 
             response_model=schemas.SuccessMessageSchema,
             dependencies=[Depends(jwt.get_current_user_from_token)])
async def activate(
    token: schemas.ActivateUserSchema, 
    db: Session= Depends(get_db)):
    
    email = jwt.decode_activate_token(token=token.token)        
    if not email:
        raise NotFound()
    
    user = crud.get_user_by_login(db, login=email)
    crud.verify_user_email(db, user.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'success': True,
            'message': "Activation Successfull!"
        } 
    )
   

@router.post("/token", 
             summary="Create token", 
             response_model=schemas.TokenSchema)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session= Depends(get_db)): 
    
    user = auth_service.authenticate_user(
        db=db, 
        login=form_data.username, 
        password=form_data.password
    )    
    if not user:
        raise NotFound()
    access_token = jwt.create_access_token(data={"sub": user.email})    
    crud.set_last_login(db, user.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "access_token": access_token, 
            "token_type": settings.JWT_TOKEN_PREFIX
        } 
    )

@router.post("/forget-password", 
             summary="Forget password")
async def forget_password(
    background_tasks: BackgroundTasks, 
    data: schemas.ForgetPasswordRequestSchema, 
    db: Session = Depends(get_db)):
       
    user = crud.get_user_by_login(db, login=data.email)
    if not user:
        raise NotFound()
    secret_token = jwt.create_reset_password_token(data={"sub": user.email})
    forget_url_link =  f"https://{settings.FRONT_HOST}/{settings.FORGET_PASSWORD_URL}/{secret_token}"
    message = forget_pwd_email(link=forget_url_link, data=data)    
    template_name = "mail/password_reset.html"        
    background_tasks.add_task(settings.fastmail.send_message, message, template_name)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Email has been sent", 
            "success": True
        }
    )    


@router.post("/reset_password/", 
             summary="Reset password", 
             response_model=schemas.SuccessMessageSchema)
async def reset_password(
    data: schemas.ResetForegetPasswordSchema, 
    db: Session= Depends(get_db)):

    email = jwt.decode_reset_password_token(token=data.secret_token)
    if not email:
        raise InvalidToken()
    if data.new_password != data.confirm_password:
        raise InvalidPassword()
    user = crud.get_user_by_login(db, login=email)
    password = security.hash_password(data.new_password)
    crud.update_user_password(db, password, user.id)
    print(datetime.now())
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'success': True, 
            'message': "Password Rest Successfull!"
        }
    )

