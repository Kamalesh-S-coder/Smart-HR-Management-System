# app/services/auth_service.py

from passlib.context import CryptContext
from prisma import Prisma
from fastapi import HTTPException
from app.schemas.auth_dtos import RootAdminCreate, EmployeeCreate, UserLogin
from app.core.security import create_access_token
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def setup_root_admin(data: RootAdminCreate):
    db = Prisma()
    await db.connect()
    
    existing_roles = await db.role.count()
    if existing_roles > 0:
        await db.disconnect()
        raise HTTPException(status_code=403, detail="System already initialized.")
        
    admin_role = await db.role.create(
        data={
            "name": "SUPER_ADMIN",
            "can_view_salaries": True,
            "can_approve_leaves": True,
            "can_revoke_devices": True,
            "can_create_users": True
        }
    )
    
    hashed_password = pwd_context.hash(data.password)
    emp_id = "EMP-0001"
    
    new_user = await db.user.create(
        data={
            "email": data.email,
            "employee_id": emp_id,
            "password_hash": hashed_password,
            "login_mode": "EMAIL_PASS",
            "role_id": admin_role.id,
            "profile": {
                "create": {
                    "full_name": data.full_name,
                    "designation": "System Administrator",
                    "department": "IT/HR"
                }
            }
        }
    )
    await db.disconnect()
    return {"message": "Root Admin successfully created!", "employee_id": emp_id}

async def onboard_employee(data: EmployeeCreate):
    db = Prisma()
    await db.connect()
    
    role = await db.role.find_unique(where={"name": data.role_name})
    if not role:
        await db.disconnect()
        raise HTTPException(status_code=404, detail=f"Role '{data.role_name}' not found.")
        
    emp_id = f"EMP-{str(uuid.uuid4())[:6].upper()}"
    hashed_password = pwd_context.hash(data.password) if data.password else None
    
    try:
        new_user = await db.user.create(
            data={
                "email": data.email,
                "employee_id": emp_id,
                "password_hash": hashed_password,
                "login_mode": data.login_mode,
                "role_id": role.id,
                "profile": {
                    "create": {
                        "full_name": data.full_name,
                        "designation": data.designation,
                        "department": data.department
                    }
                }
            }
        )
        await db.disconnect()
        return {"message": "Employee onboarded successfully!", "employee_id": emp_id}
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=400, detail="Failed to create user.")

# ---> NEW: The actual login checking logic
async def authenticate_user(data: UserLogin):
    db = Prisma()
    await db.connect()
    
    user = await db.user.find_unique(
        where={"email": data.email},
        include={"role": True}
    )
    await db.disconnect()
    
    if not user or not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
        
    access_token = create_access_token(data={"sub": user.id, "role": user.role.name})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "employee_id": user.employee_id,
        "role": user.role.name
    }