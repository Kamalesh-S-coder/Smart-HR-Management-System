from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# 1. Employee asks for time off
class LeaveRequestCreate(BaseModel):
    leave_type: str
    start_date: datetime
    end_date: datetime
    reason: Optional[str] = None

# 2. Server sends the request back to the frontend
class LeaveRequestResponse(BaseModel):
    id: str
    user_id: str
    leave_type: str
    start_date: datetime
    end_date: datetime
    status: str
    reason: Optional[str] = None
    created_at: datetime

# 3. Admin approves or rejects it
class LeaveStatusUpdate(BaseModel):
    status: str # "APPROVED" or "REJECTED"