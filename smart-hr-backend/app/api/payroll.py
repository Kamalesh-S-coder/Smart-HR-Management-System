from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from prisma import Prisma

router = APIRouter()

class PayrollCreate(BaseModel):
    employee_id: str
    month: str        # e.g., "2026-06"
    base_pay: float
    deductions: float = 0.0

@router.post("/generate", tags=["Payroll Engine"])
async def generate_payroll(data: PayrollCreate):
    db = Prisma()
    await db.connect()
    try:
        user = await db.user.find_first(where={"employee_id": data.employee_id})
        if not user:
            await db.disconnect()
            raise HTTPException(status_code=404, detail="Employee not found.")

        # Math Engine: Calculate final take-home pay
        net_pay = data.base_pay - data.deductions

        # Save to database (Matches your PayrollRecord schema)
        await db.payrollrecord.create(
            data={
                "user_id": user.id,
                "month": data.month,
                "base_pay": data.base_pay,
                "deductions": data.deductions,
                "net_pay": net_pay,
                "is_paid": False
            }
        )
        await db.disconnect()
        return {"message": f"Success! Payslip generated for {data.month}."}
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/my-payslips", tags=["Payroll Engine"])
async def get_my_payslips(employee_id: str):
    db = Prisma()
    await db.connect()
    try:
        user = await db.user.find_first(where={"employee_id": employee_id})
        if not user:
            await db.disconnect()
            raise HTTPException(status_code=404, detail="Employee not found.")
        
        payslips = await db.payrollrecord.find_many(where={"user_id": user.id})
        await db.disconnect()
        return payslips
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))