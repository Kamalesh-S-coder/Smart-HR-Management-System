import asyncio
from prisma import Prisma

async def main():
    db = Prisma()
    await db.connect()
    
    # Update the user's direct role_name field
    user = await db.user.update(
        where={'email': 'admin@company.com'},
        data={'role_name': 'Admin'}
    )
    
    print(f"Success! {user.email} is now elevated to: {user.role_name}")
    await db.disconnect()

if __name__ == '__main__':
    asyncio.run(main())