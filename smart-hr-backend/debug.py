import asyncio
from prisma import Prisma
from src.core.security import verify_password

async def main():
    db = Prisma()
    await db.connect()
    
    print("🔍 Checking database for God Account...")
    user = await db.user.find_first(where={"email": "admin@company.com"})
    
    if not user:
        print("❌ FATAL: The user is NOT in the database. The seed script failed.")
    else:
        print("✅ User found!")
        print(f"ID: {user.id}")
        print(f"Hash: {user.password_hash[:15]}...")
        
        try:
            is_valid = verify_password("Admin123!", user.password_hash)
            if is_valid:
                print("✅ MATCH: The password is 100% correct.")
                print("👉 SOLUTION: Your DB is fine. Your FastAPI server did not restart correctly. Kill the terminal (Ctrl+C) and run uvicorn again.")
            else:
                print("❌ ERROR: The password hashes do not match. The hashing library is failing.")
        except Exception as e:
            print(f"❌ CRASH: The security math failed completely. Error: {e}")
            
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())