from pydantic import BaseModel, EmailStr

# 1. Blueprint for creating an Admin
class AdminCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

# 2. Blueprint for logging in (This was missing!)
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

# 3. Blueprint for the response token (This was missing!)
class TokenResponse(BaseModel):
    access_token: str
    token_type: str