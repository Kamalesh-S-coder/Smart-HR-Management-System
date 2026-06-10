import asyncio
from src.db import get_db

async def main():
    db = get_db()
    print("Connecting to database...")
    await db.connect()
    
    try:
        # 1. Check if Admin role already exists
        print("Checking roles...")
        admin_role = await db.role.find_first(where={"name": "Admin"})
        
        # If it doesn't exist, create it cleanly
        if not admin_role:
            print("Admin role not found. Creating it...")
            admin_role = await db.role.create(
                data={
                    "name": "Admin",
                    "can_view_salaries": True,
                    "can_approve_leaves": True,
                    "can_revoke_devices": True
                }
            )
            print("✅ Admin role created.")
        else:
            print("ℹ️ Admin role already exists. Skipping role creation.")

        # 2. Check if the Admin User already exists to avoid another unique error
        print("Checking for existing Admin user...")
        admin_user = await db.user.find_first(where={"employee_id": "EMP-0001"})
        
        if not admin_user:
            print("Creating Admin user record...")
            await db.user.create(
                data={
                    "email": "admin@smart.hr",
                    "employee_id": "EMP-0001",
                    "password_hash": "admin123",  # Plain text for your development
                    "login_mode": "EMAIL_PASS",
                    "role_id": admin_role.id,
                    "isActive": True
                }
            )
            print("✅ Admin user setup complete! Email: admin@smart.hr | Pass: admin123")
        else:
            print("ℹ️ Admin user (EMP-0001) already exists. No actions taken.")

    except Exception as e:
        print(f"❌ Script crashed with error: {e}")
    finally:
        print("Disconnecting from database...")
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())