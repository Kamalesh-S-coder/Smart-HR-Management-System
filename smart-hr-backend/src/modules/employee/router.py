# src/modules/employee/router.py
from fastapi import APIRouter, HTTPException
from src.db import get_db

router = APIRouter()

@router.get("/all", tags=["Employee Directory"])
async def get_all_employees():
    db = get_db()
    await db.connect()
    try:
        users = await db.user.find_many(include={"role": True})
        
        # Format the database output to match the React table exactly
        return [
            {
                "id": u.id,
                "employee_id": u.employee_id,
                "role_name": u.role.name if u.role else "Unknown",
                "login_mode": "PASSWORD"
            }
            for u in users
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        await db.disconnect()