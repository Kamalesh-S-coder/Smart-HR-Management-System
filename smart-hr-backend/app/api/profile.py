from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from prisma import Prisma

router = APIRouter()

class ProfileUpdate(BaseModel):
    employee_id: str
    full_name: str
    phone: str
    address: str
    bank_account: str

@router.post("/update", tags=["Profile Engine"])
async def update_profile(data: ProfileUpdate):
    db = Prisma()
    await db.connect()
    try:
        # Find the user
        user = await db.user.find_first(where={"employee_id": data.employee_id})
        if not user:
            await db.disconnect()
            raise HTTPException(status_code=404, detail="Employee not found.")

        # Check if they already have a profile
        existing_profile = await db.employeeprofile.find_first(where={"user_id": user.id})
        
        if existing_profile:
            # Update existing
            await db.employeeprofile.update(
                where={"id": existing_profile.id},
                data={
                    "full_name": data.full_name,
                    "phone": data.phone,
                    "address": data.address,
                    "bank_account": data.bank_account
                }
            )
        else:
            # Create new profile
            await db.employeeprofile.create(
                data={
                    "user_id": user.id,
                    "full_name": data.full_name,
                    "phone": data.phone,
                    "address": data.address,
                    "bank_account": data.bank_account
                }
            )
        
        await db.disconnect()
        return {"message": "Profile updated successfully!"}
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))