import os
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Import the real keys
from app.core.security import SECRET_KEY
try:
    from app.core.security import ALGORITHM
except ImportError:
    ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# --- 1. STANDARD EMPLOYEE LOCK ---
async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    print("\n" + "="*40)
    print("🚀 NEW DASHBOARD REQUEST RECEIVED 🚀")
    db = request.app.state.db
    
    # Check 1: Can we read the token?
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        print(f"✅ Token Decoded! User ID: {user_id}")
        if user_id is None:
            print("❌ FAIL: User ID is missing from the token.")
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(f"❌ FAIL: Token is corrupted or uses the wrong Secret Key. Error: {e}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    # Check 2: Does the user exist in the database?
    user = await db.user.find_unique(where={"id": user_id})
    if user is None:
        print("❌ FAIL: User not found in the database.")
        raise HTTPException(status_code=401, detail="User not found")
        
    print(f"✅ User Found: {user.email} | DB Role: {user.role}")
    return user


# --- 2. HR BOSS LOCK ---
async def require_hr_clearance(current_user = Depends(get_current_user)):
    role_text = str(current_user.role)
    print(f"🔍 Checking Boss Clearance for role: '{role_text}'")
    
    # Check 3: Are they an Admin?
    if "SUPER_ADMIN" not in role_text and "ADMIN" not in role_text:
        print("❌ FAIL: Access Denied. Not an Admin.")
        raise HTTPException(status_code=403, detail="You do not have HR clearance.")
        
    print("✅ SUCCESS: Access Granted to Dashboard!")
    print("="*40 + "\n")
    return current_user