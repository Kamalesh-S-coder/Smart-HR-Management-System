from fastapi import APIRouter, HTTPException, Request, Depends
from app.schemas.user_dtos import AdminCreateRequest
from app.core.security import get_password_hash

# Import the new Bouncer
from app.api.deps import get_current_user 

router = APIRouter()

# --- 1. THE OPEN DOOR (No token needed to create the first admin) ---
@router.post("/create-super-admin", tags=["Admin Initialization"])
async def create_super_admin(request: Request, data: AdminCreateRequest):
    db = request.app.state.db

    existing_user = await db.user.find_first(
        where={"OR": [{"email": data.email}, {"username": data.username}]}
    )
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists.")

    hashed_pwd = get_password_hash(data.password)

    new_admin = await db.user.create(
        data={
            "username": data.username,
            "email": data.email,
            "password_hash": hashed_pwd,
            "role": "SUPER_ADMIN"
        }
    )

    return {
        "message": "Super Admin created successfully",
        "user_id": new_admin.id,
        "username": new_admin.username
    }

# --- 2. THE VIP LOUNGE (Protected by The Bouncer) ---
@router.get("/me", tags=["Admin Initialization"])
async def get_my_profile(current_user = Depends(get_current_user)):
    # If the code reaches this line, the token is perfectly valid!
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "status": "VIP Access Granted"
    }