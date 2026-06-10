# src/modules/leave/router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.db import get_db
from datetime import datetime, timezone

router = APIRouter()

# --- EMPLOYEE ROUTES ---
class LeaveRequestPayload(BaseModel):
    employee_id: str
    leave_type: str

@router.post("/request", tags=["Leave Management"])
async def request_leave(data: LeaveRequestPayload):
    db = get_db()
    await db.connect()
    try:
        user = await db.user.find_first(where={"employee_id": data.employee_id})
        if not user:
            raise HTTPException(status_code=404, detail="Employee ID not found.")

        await db.leaverequest.create(
            data={
                "user_id": user.id,
                "leave_type": data.leave_type,
                "status": "PENDING",
                "start_date": datetime.now(timezone.utc),
                "end_date": datetime.now(timezone.utc),
                "reason": "Standard one-day PTO request"
            }
        )
        return {"message": "PTO Request submitted successfully to Admin!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        await db.disconnect()

# --- ADMIN ROUTES ---
@router.get("/all-pending", tags=["Leave Management"])
async def get_pending_leaves():
    db = get_db()
    await db.connect()
    try:
        # Fetch leaves and include the user data so the React table can display the employee_id
        leaves = await db.leaverequest.find_many(
            where={"status": "PENDING"},
            include={"user": True} 
        )
        return leaves
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        await db.disconnect()

class UpdateStatusPayload(BaseModel):
    id: str
    status: str

@router.post("/update-status", tags=["Leave Management"])
async def update_leave_status(data: UpdateStatusPayload):
    db = get_db()
    await db.connect()
    try:
        await db.leaverequest.update(
            where={"id": data.id},
            data={"status": data.status}
        )
        return {"message": f"Leave {data.status.lower()} successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        await db.disconnect()
# Add this inside src/modules/leave/router.py
@router.get("/history/{employee_id}", tags=["Leave Management"])
async def get_employee_leave_history(employee_id: str):
    db = get_db()
    await db.connect()
    try:
        user = await db.user.find_first(where={"employee_id": employee_id})
        if not user:
            raise HTTPException(status_code=404, detail="Employee not found.")
        
        # Get all requests for this specific user
        history = await db.leaverequest.find_many(
            where={"user_id": user.id},
            order={"start_date": "desc"}
        )
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await db.disconnect()