# app/schemas/auth_dtos.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class RootAdminCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class EmployeeCreate(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    role_name: str           
    login_mode: str          
    password: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None

# ---> NEW: We added this so the API knows what login data looks like
class UserLogin(BaseModel):
    email: str
    password: str