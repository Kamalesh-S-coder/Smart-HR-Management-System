from typing import Optional
from pydantic import BaseModel, EmailStr

# 1. Onboarding Blueprint
class EmployeeOnboardRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    designation: str
    salary: float

# 2. Nested HR Profile
class ProfileResponse(BaseModel):
    first_name: str
    last_name: str
    designation: str
    salary: Optional[float] = None

# 3. Employee List Blueprint
class EmployeeListResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_active: bool
    profile: Optional[ProfileResponse] = None

# 4. Smart Update Blueprint
class EmployeeUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    designation: Optional[str] = None
    salary: Optional[float] = None