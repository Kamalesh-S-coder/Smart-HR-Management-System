from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, dashboard, leave, attendance, payroll, shift, profile, stats, device

app = FastAPI(title="Smart HR API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(dashboard.router, prefix="/api/dashboard")
app.include_router(leave.router, prefix="/api/leave")
app.include_router(attendance.router, prefix="/api/attendance")
app.include_router(payroll.router, prefix="/api/payroll")
app.include_router(shift.router, prefix="/api/shift")
app.include_router(profile.router, prefix="/api/profile")
app.include_router(stats.router, prefix="/api/stats")
app.include_router(device.router, prefix="/api/device") # THE ABSOLUTE FINAL WIRE