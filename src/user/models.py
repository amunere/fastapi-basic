from sqlalchemy import Column, DateTime, Integer, String, Boolean
from src.database import Base
from datetime import datetime


class User(Base):
    """Models a user table"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    password = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    email_verified = Column(Boolean(), default=False)
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean, default=False)
    first_name = Column(String(50), nullable=True)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=False)
    time_created = Column(DateTime, default=datetime.now())
    time_updated = Column(DateTime, onupdate=datetime.now()) 


    def __repr__(self):
        return f"<Hi {self.username}>"