from fastapi import APIRouter, Depends, HTTPException, Request
from app.api.deps import get_current_user, require_hr_clearance
from app.schemas.employee_dtos import EmployeeOnboardRequest, EmployeeListResponse, EmployeeUpdateRequest
from app.core.security import get_password_hash 

router = APIRouter()

# --- 1. ONBOARD NEW EMPLOYEE ---
@router.post("/onboard", tags=["HR Management"])
async def onboard_employee(
    request: Request,
    data: EmployeeOnboardRequest,
    # This single line locks the door!
    current_user = Depends(require_hr_clearance)
):
    db = request.app.state.db
    
    # 1. Check if the username or email is already taken
    existing_user = await db.user.find_first(
        where={"OR": [{"email": data.email}, {"username": data.username}]}
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already taken")

    # 2. Create the user and their nested HR profile
    new_user = await db.user.create(
        data={
            "username": data.username,
            "email": data.email,
            "password_hash": get_password_hash(data.password),
            "role": "EMPLOYEE",
            "is_active": True,
            "profile": {
                "create": {
                    "first_name": data.first_name,
                    "last_name": data.last_name,
                    "designation": data.designation,
                    "salary": data.salary
                }
            }
        },
        include={"profile": True}
    )
    return new_user


# --- 2. GET ALL EMPLOYEES ---
@router.get("/all", tags=["HR Management"])
async def get_all_employees(
    request: Request,
    current_user = Depends(require_hr_clearance)
):
    db = request.app.state.db
    
    employees = await db.user.find_many(
        include={"profile": True}
    )
    return employees


# --- 3. UPDATE EMPLOYEE PROFILE ---
@router.patch("/{employee_id}/update", tags=["HR Management"])
async def update_employee_profile(
    employee_id: str, 
    update_data: EmployeeUpdateRequest, 
    request: Request, 
    current_user = Depends(require_hr_clearance)
):
    db = request.app.state.db

    # 1. Verify the employee actually exists
    employee = await db.user.find_unique(
        where={"id": employee_id},
        include={"profile": True}
    )
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")
        
    if not employee.is_active:
        raise HTTPException(status_code=400, detail="Cannot update a deactivated employee.")

    # 2. Extract ONLY the fields that HR actually sent
    update_dict = update_data.model_dump(exclude_unset=True)

    if not update_dict:
        raise HTTPException(status_code=400, detail="No new data provided to update.")

    # 3. Apply the partial update to the nested HR profile
    updated_profile = await db.profile.update(
        where={
            "user_id": employee_id
        },
        data=update_dict
    )

    return {
        "message": "Employee profile successfully updated.",
        "updated_fields": update_dict
    }