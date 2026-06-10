from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.db import get_db
from datetime import datetime, timezone
import calendar

router = APIRouter()

class PayrollExecutePayload(BaseModel):
    target_user_id: str
    month: str
    hourly_rate: float  # We swapped base_pay for hourly_rate!
    admin_id: str

@router.post("/execute", tags=["Payroll"])
async def execute_payroll(data: PayrollExecutePayload):
    db = get_db()
    await db.connect()
    
    try:
        # 1. Securely find the employee
        user = await db.user.find_first(where={"employee_id": data.target_user_id})
        if not user:
            raise HTTPException(status_code=404, detail="Employee not found.")

        # 2. Build the exact Time Window for the requested month
        year, month_num = map(int, data.month.split('-'))
        start_date = datetime(year, month_num, 1, tzinfo=timezone.utc)
        last_day = calendar.monthrange(year, month_num)[1]
        end_date = datetime(year, month_num, last_day, 23, 59, 59, tzinfo=timezone.utc)

        # 3. Sweep the Attendance Table
        attendance_records = await db.attendancerecord.find_many(
            where={
                "user_id": user.id,
                "clock_in": {"gte": start_date, "lte": end_date},
                "clock_out": {"not": None} # Only grab completed shifts!
            }
        )

        # 4. Calculate total hours worked
        total_seconds_worked = 0
        for record in attendance_records:
            shift_duration = record.clock_out - record.clock_in
            total_seconds_worked += shift_duration.total_seconds()
            
        total_hours = total_seconds_worked / 3600

        # 5. Financial Math
        gross_pay = total_hours * data.hourly_rate
        net_pay = gross_pay * 0.85 # 15% tax deduction

        # 6. Save the record
        await db.payrollrecord.create(
            data={
                "user": {"connect": {"id": user.id}},       
                "month": data.month,      
                "base_pay": gross_pay, # Storing the calculated gross pay to satisfy Prisma schema
                "net_pay": net_pay,
                "salary_model": "HOURLY" # Changed from MONTHLY to HOURLY
            }
        )
        
        return {
            "message": f"Calculated {round(total_hours, 2)} hours. Payroll executed!", 
            "net_pay": round(net_pay, 2)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        await db.disconnect()