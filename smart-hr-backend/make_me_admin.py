# make_me_admin.py
import asyncio
from prisma import Prisma

async def main():
    db = Prisma()
    await db.connect()
    
    print("👑 Forcing God Mode Role Assignment...")
    
    # 1. Find the Super Admin role in the database
    admin_role = await db.role.find_first(where={"name": "Super Admin"})
    
    if not admin_role:
        print("❌ FATAL: Super Admin role does not exist. Run seed.py again.")
    else:
        # 2. Forcefully attach it to your account
        await db.user.update(
            where={"email": "admin@company.com"},
            data={"role_id": admin_role.id}
        )
        print("✅ SUCCESS: Your account has been permanently upgraded to Super Admin!")
        print("👉 You must now go log in ONE MORE TIME to get your new upgraded Access Token.")
        
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())