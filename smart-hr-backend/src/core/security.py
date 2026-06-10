# src/core/security.py
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext

# In a real enterprise app, this lives in your .env file
SECRET_KEY = "enterprise_super_secret_key_change_me_in_production"
ALGORITHM = "HS256"

# This sets up bcrypt, the industry standard for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=12)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)