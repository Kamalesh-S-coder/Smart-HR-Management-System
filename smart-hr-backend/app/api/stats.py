from fastapi import APIRouter, HTTPException
from prisma import Prisma

router = APIRouter()

@router.get("/overview", tags=["Admin Analytics"])
async def get_system_stats():
    db = Prisma()
    await db.connect()
    try:
        # Count total registered users
        total_employees = await db.user.count()
        
        # Count only leaves that need action
        pending_leaves = await db.leaverequest.count(where={"status": "PENDING"})
        
        # Calculate total money spent on payroll across the whole company
        all_payroll = await db.payrollrecord.find_many()
        total_spent = sum([p.net_pay for p in all_payroll])

        await db.disconnect()
        
        return {
            "total_employees": total_employees,
            "pending_leaves": pending_leaves,
            "total_payroll_spent": round(total_spent, 2)
        }
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))