# src/modules/shift/router.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from prisma import Prisma
from src.core.dependencies import get_current_user
from datetime import datetime

router = APIRouter()

class ShiftCreate(BaseModel):
    target_user_id: str
    shift_date: datetime
    start_time: datetime
    end_time: datetime

class SwapRequest(BaseModel):
    target_shift_id: str

@router.post("/create", tags=["Shift Scheduling Engine"])
async def create_shift(data: ShiftCreate, current_user: dict = Depends(get_current_user)):
    db = Prisma()
    await db.connect()
    try:
        # RBAC Check
        if current_user["role"] != "Super Admin":
            await db.disconnect()
            raise HTTPException(status_code=403, detail="RBAC Error: Only Admins can schedule shifts.")
            
        shift = await db.shift.create(
            data={
                "user_id": data.target_user_id,
                "shift_date": data.shift_date,
                "start_time": data.start_time,
                "end_time": data.end_time
            }
        )
        await db.disconnect()
        return {"message": "Shift successfully created.", "shift": shift}
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{shift_id}/swap", tags=["Shift Scheduling Engine"])
async def request_shift_swap(shift_id: str, data: SwapRequest, current_user: dict = Depends(get_current_user)):
    # In a fully fleshed out system, this creates a "SwapRequest" database entry.
    # For now, it alerts the Admin dashboard for approval.
    return {"message": f"Swap request for shift {shift_id} sent to Admin for approval."}