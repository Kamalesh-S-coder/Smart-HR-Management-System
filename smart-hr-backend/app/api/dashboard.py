# app/api/dashboard.py

from fastapi import APIRouter, Depends
from prisma import Prisma
from app.core.security import require_permission

router = APIRouter()

# Protected route: Only Admins can see this specific God Mode dashboard
@router.get("/stats", tags=["Dashboard"])
async def get_dashboard_stats(
    current_user: dict = Depends(require_permission("can_create_users"))
):
    db = Prisma()
    await db.connect()
    
    try:
        # Count total active employees (all users for now)
        total_employees = await db.user.count()
        
        # Count all Leave Requests sitting in "PENDING" status
        pending_leaves = await db.leaverequest.count(where={"status": "PENDING"})
        
        await db.disconnect()
        
        return {
            "active_employees": total_employees,
            "pending_leaves": pending_leaves
        }
    except Exception as e:
        await db.disconnect()
        return {"active_employees": "Error", "pending_leaves": "Error"}