from sqlalchemy.orm import Session
from src.user import crud
from src.auth import security


class Authenticate():  
    
    def authenticate_user(self, db: Session, login: str, password: str):
        user = crud.get_user_by_login(db, login) 
        if not user:
            return False
        if not security.verify_password(password, user.password):
            return False
        return user
    


    
    

    
