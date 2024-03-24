from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.config import settings
from jose import JWTError, jwt
from src.constants import ErrorMessage as error

from src.database import get_db
from src.user import crud
from src.user.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", scheme_name="JWT")


"""Create token for login"""
def create_access_token(
        data: dict, 
        expires_delta: Optional[timedelta] = None
    ):

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else             :
        expire = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt  


"""Check user from token"""
def get_current_user_from_token(
        token: str = Depends(oauth2_scheme), 
        db: str = Depends(get_db) 
    ): 
   
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=error.INVALID_CREDENTIALS,
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_login(login=email, db=db)
    if user is None:
        raise credentials_exception
    return user

CurrentUser = Annotated[User, Depends(get_current_user_from_token)]

"""Create Activate token"""
def create_activate_token(
        data: dict, 
        expires_delta: Optional[timedelta] = None
    ):

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(
            minutes=30
        )
    to_encode.update({"exp": expire})
    token = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        settings.JWT_ALGORITHM)
    return token


"""Decode Activate token"""
def decode_activate_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None


"""Create reset password token"""
def create_reset_password_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(
            minutes=settings.RESET_PWD_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    token = jwt.encode(
        to_encode, 
        settings.FORGET_PWD_SECRET_KEY, 
        settings.JWT_ALGORITHM)
    return token


"""Decode reset password token"""
def decode_reset_password_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.FORGET_PWD_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None 





