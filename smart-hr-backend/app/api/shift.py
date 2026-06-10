from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from prisma import Prisma
from datetime import datetime, timezone

router = APIRouter()

class ShiftCreate(BaseModel):
    employee_id: str
    shift_date: str  # Format: "YYYY-MM-DD"
    start_time: str  # Format: "HH:MM"
    end_time: str    # Format: "HH:MM"

@router.post("/assign", tags=["Shift Scheduling"])
async def assign_shift(data: ShiftCreate):
    db = Prisma()
    await db.connect()
    try:
        user = await db.user.find_first(where={"employee_id": data.employee_id})
        if not user:
            await db.disconnect()
            raise HTTPException(status_code=404, detail="Employee not found.")

        # Convert simple strings into strict Postgres UTC DateTimes
        shift_dt = datetime.strptime(data.shift_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        start_dt = datetime.strptime(f"{data.shift_date} {data.start_time}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        end_dt = datetime.strptime(f"{data.shift_date} {data.end_time}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)

        # Map to your schema's Shift model
        await db.shift.create(
            data={
                "user_id": user.id,
                "shift_date": shift_dt,
                "start_time": start_dt,
                "end_time": end_dt
            }
        )
        await db.disconnect()
        return {"message": f"Success! Shift assigned for {data.shift_date}."}
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/my-schedule", tags=["Shift Scheduling"])
async def get_my_schedule(employee_id: str):
    db = Prisma()
    await db.connect()
    try:
        user = await db.user.find_first(where={"employee_id": employee_id})
        if not user:
            await db.disconnect()
            raise HTTPException(status_code=404, detail="Employee not found.")
        
        # Get shifts and sort them by date
        shifts = await db.shift.find_many(
            where={"user_id": user.id},
            order={"shift_date": "asc"}
        )
        await db.disconnect()
        return shifts
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))