from pydantic import BaseModel, EmailStr, Field


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    email: EmailStr | None = None


class ForgetPasswordRequestSchema(BaseModel):
    email: EmailStr | None = None


class VerifyUserSchema(BaseModel):
    email: EmailStr | None = None


class ActivateUserSchema(BaseModel):
    token: str | None = None


class ResetForegetPasswordSchema(BaseModel):
    secret_token: str
    new_password: str = Field(min_length=8, max_length=100)
    confirm_password: str = Field(min_length=8, max_length=100)


class SuccessMessageSchema(BaseModel):
    success: bool
    status_code: int
    message: str