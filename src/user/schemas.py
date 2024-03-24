from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing import Optional


class UserBaseSchema(BaseModel):
    username: str
    email: Optional[EmailStr]      


class UserSchema(UserBaseSchema):
    """
    Email, and password are required for create a new user,
    Password are required for logging in the user
    """
    password: str = Field(min_length=8, max_length=100)


class UserPublicSchema(UserBaseSchema):
    email: EmailStr | None
    username: str | None
    first_name: str | None
    middle_name: str | None
    last_name: str | None

class UserUpdateSchema(BaseModel):
    first_name: Optional[str] 
    middle_name: Optional[str] 
    last_name: Optional[str] 
