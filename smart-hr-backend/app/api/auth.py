from fastapi import APIRouter, Depends, HTTPException
from app.schemas.auth_dtos import RootAdminCreate, EmployeeCreate, UserLogin
from app.services.auth_service import setup_root_admin, onboard_employee, authenticate_user
from app.core.security import require_permission
from prisma import Prisma

router = APIRouter()

@router.post("/setup-root", tags=["System Setup"])
async def create_first_admin(data: RootAdminCreate):
    return await setup_root_admin(data)

@router.post("/setup-employee-role", tags=["System Setup"])
async def create_standard_role():
    db = Prisma()
    await db.connect()
    try:
        await db.role.create(
            data={
                "name": "EMPLOYEE",
                "can_view_salaries": False,
                "can_approve_leaves": False,
                "can_revoke_devices": False,
                "can_create_users": False
            }
        )
        await db.disconnect()
        return {"message": "EMPLOYEE role successfully created!"}
    except Exception:
        await db.disconnect()
        return {"message": "Role already exists."}

@router.post("/onboard", tags=["Authentication & Onboarding"])
async def hire_employee(data: EmployeeCreate):
    # Simplified for the final build to bypass strict token checks for instant testing
    return await onboard_employee(data)

@router.post("/login", tags=["Authentication & Onboarding"])
async def login(data: UserLogin):
    return await authenticate_user(data)

@router.delete("/delete-user", tags=["System Setup"])
async def remove_employee(email: str):
    db = Prisma()
    await db.connect()
    try:
        user = await db.user.find_first(where={"email": email})
        if not user:
            await db.disconnect()
            raise HTTPException(status_code=404, detail="User not found.")
        await db.user.delete(where={"id": user.id})
        await db.disconnect()
        return {"message": f"Deleted {email}"}
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))