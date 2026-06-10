from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from prisma import Prisma
from datetime import datetime, timezone

router = APIRouter()

class LeaveRequestCreate(BaseModel):
    employee_id: str
    start_date: str
    end_date: str
    reason: str
    leave_type: str

class LeaveStatusUpdate(BaseModel):
    leave_id: str
    status: str  # "APPROVED" or "REJECTED"

@router.post("/request", tags=["Leave Management"])
async def submit_leave_request(data: LeaveRequestCreate):
    db = Prisma()
    await db.connect()
    try:
        user = await db.user.find_first(where={"employee_id": data.employee_id})
        if not user:
            await db.disconnect()
            raise HTTPException(status_code=404, detail="Employee not found.")

        start_dt = datetime.strptime(data.start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end_dt = datetime.strptime(data.end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)

        await db.leaverequest.create(
            data={
                "status": "PENDING",
                "user_id": user.id,            
                "leave_type": data.leave_type, 
                "start_date": start_dt,        
                "end_date": end_dt,            
                "reason": data.reason
            }
        )
        await db.disconnect()
        return {"message": "Leave request submitted successfully!"}
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))

# ---> NEW ROUTE: Fetch leaves for a specific employee <---
@router.get("/my-leaves", tags=["Leave Management"])
async def get_my_leaves(employee_id: str):
    db = Prisma()
    await db.connect()
    try:
        # Find the user first
        user = await db.user.find_first(where={"employee_id": employee_id})
        if not user:
            await db.disconnect()
            raise HTTPException(status_code=404, detail="User not found.")
        
        # Get only this user's leaves
        leaves = await db.leaverequest.find_many(where={"user_id": user.id})
        await db.disconnect()
        return leaves
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all", tags=["Leave Management"])
async def get_all_pending_leaves():
    db = Prisma()
    await db.connect()
    try:
        leaves = await db.leaverequest.find_many(where={"status": "PENDING"})
        await db.disconnect()
        return leaves
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update-status", tags=["Leave Management"])
async def update_leave_status(data: LeaveStatusUpdate):
    db = Prisma()
    await db.connect()
    try:
        await db.leaverequest.update(
            where={"id": data.leave_id},
            data={"status": data.status}
        )
        await db.disconnect()
        return {"message": f"Leave has been {data.status}"}
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))