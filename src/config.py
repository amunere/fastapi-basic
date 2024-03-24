from typing import Any, Dict, List, Optional
from fastapi.templating import Jinja2Templates
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi_mail import ConnectionConfig, FastMail

class Settings(BaseSettings):
    
    #Base settings
    APP_NAME: str 
    APP_HOST: str
    FRONT_HOST: str
    ADMIN_EMAIL: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    #Mail settings
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool
    TEMPLATE_FOLDER: str

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str      
    
    JWT_SETTINGS: Optional[Dict[str, Any]] = None
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    JWT_TOKEN_PREFIX: str
    JWT_AUDIENCE: str
    JWT_SECRET_KEY: str  
    JWT_REFRESH_SECRET_KEY: str

    RESET_PWD_TOKEN_EXPIRE_MINUTES: int
    FORGET_PWD_SECRET_KEY: str
    FORGET_PASSWORD_URL: str = "reset_password"
   
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore', env_nested_delimiter='__')
    

    @property
    def sync_database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        
    @property
    def fastmail(self):
        mail_conf = ConnectionConfig(    
            MAIL_USERNAME = self.MAIL_USERNAME,
            MAIL_PASSWORD = self.MAIL_PASSWORD,
            MAIL_FROM = self.MAIL_FROM,
            MAIL_PORT = self.MAIL_PORT,
            MAIL_SERVER = self.MAIL_SERVER,
            MAIL_STARTTLS = self.MAIL_STARTTLS,
            MAIL_SSL_TLS = self.MAIL_SSL_TLS,
            USE_CREDENTIALS = self.USE_CREDENTIALS,
            VALIDATE_CERTS = self.VALIDATE_CERTS,
            TEMPLATE_FOLDER = self.TEMPLATE_FOLDER,
        )
        fm = FastMail(mail_conf)
        return fm
    
    @property
    def get_templates(self):
        templates = Jinja2Templates(directory="templates")
        return templates


settings = Settings()
