from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.modules.leave.router import router as leave_router
from src.modules.employee.router import router as employee_router
from src.modules.auth.router import router as auth_router 
from src.modules.attendance.router import router as attendance_router
from src.modules.payroll.router import router as payroll_router # <-- ADD THIS

app = FastAPI(title="Smart HR API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth") 
app.include_router(leave_router, prefix="/api/v1/leave")
app.include_router(employee_router, prefix="/api/v1/employee")
app.include_router(attendance_router, prefix="/api/v1/attendance")
app.include_router(payroll_router, prefix="/api/v1/payroll") # <-- ADD THIS

@app.get("/")
def read_root():
    return {"status": "Backend is running flawlessly"}