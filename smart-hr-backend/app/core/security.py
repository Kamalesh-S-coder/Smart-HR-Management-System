# app/core/security.py

import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from prisma import Prisma

# In a real production app, this lives in the .env file
SECRET_KEY = "your-super-secret-enterprise-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# THE RBAC DEPENDENCY GENERATOR
def require_permission(permission: str):
    async def permission_checker(current_user: dict = Depends(get_current_user)):
        db = Prisma()
        await db.connect()
        
        user = await db.user.find_unique(
            where={"id": current_user["sub"]},
            include={"role": True}
        )
        
        await db.disconnect()
        
        if not user or not getattr(user.role, permission, False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Requires: {permission}"
            )
        return user
    return permission_checker