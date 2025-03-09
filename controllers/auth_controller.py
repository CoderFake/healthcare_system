from database.models import User
from typing import Optional, Callable, Dict, Any
from utils.helpers import verify_password

class AuthController:
    def __init__(self):
        self.current_user = None
    
    def login(self, username: str, password: str) -> bool:
        user = User.find_by_username(username)
        
        if user and verify_password(password, user.pass_):
            self.current_user = user
            return True
        return False
    
    def logout(self):
        self.current_user = None
    
    def is_authenticated(self) -> bool:
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[User]:
        return self.current_user
    
    def is_admin(self) -> bool:
        if not self.current_user:
            return False
        return getattr(self.current_user, 'Quyen', '') == 'admin'
    
    def is_doctor(self) -> bool:
        if not self.current_user:
            return False
        return getattr(self.current_user, 'Quyen', '') == 'doctor'
    
    def is_staff(self) -> bool:
        if not self.current_user:
            return False
        return getattr(self.current_user, 'Quyen', '') == 'staff'
    
    def change_password(self, old_password: str, new_password: str) -> bool:
        if not self.is_authenticated():
            return False
            
        if not verify_password(old_password, self.current_user.pass_):
            return False
            
        return self.current_user.update_password(new_password)
    
    def reset_password(self, username: str, new_password: str) -> bool:
        if not self.is_admin():
            return False
            
        user = User.find_by_username(username)
        if not user:
            return False
            
        return user.update_password(new_password)