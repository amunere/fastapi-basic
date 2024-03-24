from typing import Optional 
from fastapi import Depends, APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.auth import jwt, security
from src.exceptions import (
    NotFound, 
    DuplicateRecord, 
    PermissionDenied
)
from src.user import crud, schemas
from src.database import get_db

router = APIRouter()


@router.get("/", summary="Get all users", 
            response_model=list[schemas.UserPublicSchema], 
            dependencies=[Depends(jwt.get_current_user_from_token)])
async def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/create", 
             summary="Create new user", 
             response_model=schemas.UserPublicSchema)
async def create_user(
    user: schemas.UserSchema, 
    db: Session = Depends(get_db)):    
    
    try:
        user.password = security.hash_password(user.password)
        return crud.create_user(db, user)
    except:
        raise DuplicateRecord()
    

@router.get("/me", 
            summary="Get current user", 
            response_model=schemas.UserPublicSchema)
async def get_user(current_user: jwt.CurrentUser):      
    return current_user


@router.get("/search", 
            summary="Search user by email or username", 
            dependencies=[Depends(jwt.get_current_user_from_token)], 
            response_model=list[schemas.UserPublicSchema])
async def search_user(
    f: Optional[str] = None, 
    max_results: Optional[int] = 30, 
    db: Session=Depends(get_db), 
    skip: int = 0, 
    limit: int = 100):
    
    users = crud.get_users(db, skip=skip, limit=limit)  
    if not f:
        return users[:max_results]    
    
    results = list(filter(lambda user: (f.lower() in user.email or f.lower() in user.username), users))
    return results[:max_results]


@router.put("/update", 
            response_model=schemas.UserPublicSchema,
            summary="Update user first, middle and last name")
async def update_user(
    user_data: schemas.UserUpdateSchema,
    current_user: jwt.CurrentUser,
    db: Session = Depends(get_db)):  
    
    if not current_user:
        raise NotFound()
    return crud.update_user_fml(db, user_data, id=current_user.id)
    

@router.get("/{id}", 
            response_model=schemas.UserPublicSchema, 
            summary="Get user by ID")
async def get_user_by_id(
    id: int, 
    current_user: jwt.CurrentUser, 
    db: Session = Depends(get_db)):    
    user = crud.get_user_by_id(db, id)  
    if not user:
        raise NotFound()    
    if not current_user.is_superuser and (current_user.id != user.id):
        raise PermissionDenied()
    return user    


@router.delete("/{id}", 
            summary="Delete user by ID", 
            dependencies=[Depends(jwt.get_current_user_from_token)])
async def delete_user_by_id(
    id: int, 
    current_user: jwt.CurrentUser, 
    db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, id)  
    if not user:
        raise PermissionDenied()
    elif user != current_user and not current_user.is_superuser:
        raise PermissionDenied()
    elif user == current_user and current_user.is_superuser:
        raise PermissionDenied()
    crud.delete_user(db, id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'success': True, 
            'message': "User deleted successfully!"
        }
    )
