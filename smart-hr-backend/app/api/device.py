from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from prisma import Prisma

router = APIRouter()

class DeviceLogCreate(BaseModel):
    employee_id: str
    device_os: str
    browser: str

@router.post("/log", tags=["Security Engine"])
async def log_device(data: DeviceLogCreate):
    db = Prisma()
    await db.connect()
    try:
        user = await db.user.find_first(where={"employee_id": data.employee_id})
        if not user:
            await db.disconnect()
            raise HTTPException(status_code=404, detail="User not found")

        # Save to the final table in your database
        await db.devicefingerprint.create(
            data={
                "user_id": user.id,
                "device_os": data.device_os,
                "browser": data.browser,
                "ip_address": "127.0.0.1", # Mock IP for local testing
                "is_active": True
            }
        )
        await db.disconnect()
        return {"message": "Device secured and logged."}
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/active", tags=["Security Engine"])
async def get_active_devices():
    db = Prisma()
    await db.connect()
    try:
        # Fetch active devices
        devices = await db.devicefingerprint.find_many(
            where={"is_active": True}
        )
        await db.disconnect()
        return devices
    except Exception as e:
        await db.disconnect()
        raise HTTPException(status_code=500, detail=str(e))