from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from prisma import Prisma
from datetime import datetime, timezone

router = APIRouter()

class ClockInRequest(BaseModel):
    employee_id: str
    work_mode: str  # "OFFICE" or "REMOTE"

class ClockOutRequest(BaseModel):
    employee_id: str

@router.post("/clock-in", tags=["Attendance Engine"])
async def clock_in(data: ClockInRequest):
    db = Prisma()
    await db.connect()
    try:
        user = await db.user.find_first(where={"employee_id": data.employee_id})
        if not user:
            await db.disconnect()
            raise HTTPException(status_code=404, detail="User not found")
        
        now = datetime.now(timezone.utc)
        
        # Matches your AttendanceRecord schema perfectly
        await db.attendancerecord.create(
            data={
                "user_id": user.id,
                "date": now,
                "clock_in": now,
                "work_mode": data.work_mode,
                "is_anomaly": False
            }
        )
        await db.disconnect()
        return {"message": f"Successfully clocked in for {data.work_mode} work!"}
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clock-out", tags=["Attendance Engine"])
async def clock_out(data: ClockOutRequest):
    db = Prisma()
    await db.connect()
    try:
        user = await db.user.find_first(where={"employee_id": data.employee_id})
        if not user:
            await db.disconnect()
            raise HTTPException(status_code=404, detail="User not found")
        
        # Find the active shift (where they haven't clocked out yet)
        record = await db.attendancerecord.find_first(
            where={"user_id": user.id, "clock_out": None},
            order={"clock_in": "desc"}
        )
        
        if not record:
            await db.disconnect()
            raise HTTPException(status_code=400, detail="You are not currently clocked in.")
        
        now = datetime.now(timezone.utc)
        await db.attendancerecord.update(
            where={"id": record.id},
            data={"clock_out": now}
        )
        await db.disconnect()
        return {"message": "Successfully clocked out!"}
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))