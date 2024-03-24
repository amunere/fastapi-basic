from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.user import models, schemas
from passlib.context import CryptContext
from datetime import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


"""Get user by id"""
def get_user_by_id(db: Session, id: int): 
    return db.query(models.User).filter(models.User.id == id).one_or_none()

"""Get user by email or username"""
def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(or_(models.User.email == login, models.User.username == login)).one_or_none()

"""Get all users"""
def get_users(db: Session, skip: int = 0, limit: int = 100):    
    return db.query(models.User).offset(skip).limit(limit).all()


"""Create new user"""
def create_user(db: Session, user: schemas.UserSchema):
    user_instance = models.User(**user.model_dump())    
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance


"""Set last login"""
def set_last_login(db: Session, id: int):
    user_instance = db.query(models.User).filter(models.User.id == id).one_or_none()
    user_instance.last_login = datetime.now()  
    db.add(user_instance)
    db.commit()
    return 



"""Activate user"""
def verify_user_email(db: Session, id: int):
    user_instance = db.query(models.User).filter(models.User.id == id).one_or_none()
    user_instance.email_verified = True    
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance


"""Update user first, middle and last name"""
def update_user_fml(db: Session, user_data: schemas.UserUpdateSchema, id: int):
    user_instance = db.query(models.User).filter(models.User.id == id).one_or_none()
    if user_instance is None:
        return None
    for k, v in vars(user_data).items():
        setattr(user_instance, k, v) if v else None
    
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance
   
    
"""Update user password"""
def update_user_password(db: Session, password: schemas.UserUpdateSchema, id: int):
    user_instance = db.query(models.User).filter(models.User.id == id).one_or_none()
    user_instance.password = password
    
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance


"""Delete user"""
def delete_user(db: Session, id: int):
    user_instance = db.query(models.User).filter(models.User.id == id).one_or_none()
    db.delete(user_instance)
    db.commit()
    return 