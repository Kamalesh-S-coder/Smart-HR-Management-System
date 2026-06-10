from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.db import get_db

router = APIRouter()

class OnboardRequest(BaseModel):
    fullName: str
    email: str
    role: str

@router.post("/request", tags=["Onboarding"])
async def request_onboarding(data: OnboardRequest):
    db = get_db()
    await db.connect()
    try:
        await db.employeerequest.create(data={
            "fullName": data.fullName,
            "email": data.email,
            "role": data.role
        })
        return {"message": "Request submitted! Admin will review."}
    finally:
        await db.disconnect()

@router.post("/hire/{request_id}", tags=["Onboarding"])
async def hire_employee(request_id: str):
    db = get_db()
    await db.connect()
    try:
        req = await db.employeerequest.find_unique(where={"id": request_id})
        if not req:
            raise HTTPException(status_code=404, detail="Request not found")
        
        # Create user with active status
        new_user = await db.user.create(data={
            "employee_id": f"EMP-{req.fullName[:3].upper()}{req.id[:4].upper()}",
            "email": req.email,
            "password": "default_password_123", 
            "isActive": True
        })
        
        # Approve request
        await db.employeerequest.update(where={"id": request_id}, data={"status": "APPROVED"})
        return {"message": f"Hired {req.fullName} successfully!"}
    finally:
        await db.disconnect()

@router.post("/terminate/{user_id}", tags=["Onboarding"])
async def terminate_employee(user_id: str):
    db = get_db()
    await db.connect()
    try:
        await db.user.update(
            where={"id": user_id},
            data={"isActive": False}
        )
        return {"message": "Employee access revoked."}
    finally:
        await db.disconnect()