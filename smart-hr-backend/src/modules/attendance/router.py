# src/modules/attendance/router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.db import get_db
from datetime import datetime, timezone

router = APIRouter()

class ClockInRequest(BaseModel):
    employee_id: str
    work_mode: str

@router.post("/clock-in", tags=["Smart Attendance"])
async def clock_in(data: ClockInRequest):
    db = get_db()
    await db.connect()
    try:
        user = await db.user.find_first(where={"employee_id": data.employee_id})
        if not user:
            raise HTTPException(status_code=404, detail="Employee ID not found.")

        await db.attendancerecord.create(
            data={
                "user": {"connect": {"id": user.id}},
                "clock_in": datetime.now(timezone.utc),
                "work_mode": data.work_mode
            }
        )
        return {"message": f"Success: {user.employee_id} clocked in securely!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        await db.disconnect()

# --- THE NEW CLOCK OUT ENGINE ---
@router.post("/clock-out", tags=["Smart Attendance"])
async def clock_out(data: ClockInRequest):
    db = get_db()
    await db.connect()
    try:
        user = await db.user.find_first(where={"employee_id": data.employee_id})
        if not user:
            raise HTTPException(status_code=404, detail="Employee ID not found.")

        # Find the most recent clock-in record for this user
        record = await db.attendancerecord.find_first(
            where={"user_id": user.id},
            order={"clock_in": "desc"}
        )
        
        if not record:
            raise HTTPException(status_code=400, detail="No active clock-in found.")

        # Update that record with the exact clock-out time
        await db.attendancerecord.update(
            where={"id": record.id},
            data={"clock_out": datetime.now(timezone.utc)}
        )
        return {"message": f"Successfully clocked out. Have a great evening!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        await db.disconnect()