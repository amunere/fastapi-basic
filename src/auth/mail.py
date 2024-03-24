from fastapi_mail import MessageSchema, MessageType
from src.config import settings
from .constants import MailDetail


"""Message for forget password"""
def forget_pwd_email(link: str, data: dict):
    email_body = {
        "app_name": settings.APP_NAME,
        "link_expiry_min": settings.RESET_PWD_TOKEN_EXPIRE_MINUTES,
        "reset_link": link,
        "app_host": settings.FRONT_HOST,
    }        
    message = MessageSchema(
        subject=f"{MailDetail.FORGET_PWD_MAIL_SUBJECT}{settings.FRONT_HOST}",
        recipients=[data.email],
        template_body=email_body,
        subtype=MessageType.html
    )       
    return message

"""Message for verify user email"""
def verify_email(link: str, user: dict):
    email_body = {
        "app_name": settings.APP_NAME,
        "link": link,
        "app_host": settings.FRONT_HOST,
        "first_name": user.first_name,
    }        
    message = MessageSchema(
        subject=f"{MailDetail.VERIFY_MAIL_SUBJECT}{settings.FRONT_HOST}",
        recipients=[user.email],
        template_body=email_body,
        subtype=MessageType.html
    )       
    return message