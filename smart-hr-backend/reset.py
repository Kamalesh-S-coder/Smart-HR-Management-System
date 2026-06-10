# reset.py
import asyncio
from prisma import Prisma
from src.core.security import get_password_hash, verify_password

async def main():
    db = Prisma()
    await db.connect()
    
    print("🔨 Forcing an absolute password reset...")
    fresh_hash = get_password_hash("Admin123!")
    
    # Force the database to overwrite whatever is in there
    await db.user.update(
        where={"email": "admin@company.com"},
        data={"password_hash": fresh_hash}
    )
    
    # Verify it immediately
    user = await db.user.find_first(where={"email": "admin@company.com"})
    if verify_password("Admin123!", user.password_hash):
        print("✅ SUCCESS: Hash overwritten and verified perfectly.")
        print("👉 Server is ready. Go test the Swagger UI right now.")
    else:
        print("❌ FATAL: The Python bcrypt library is failing on your OS.")
        
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())