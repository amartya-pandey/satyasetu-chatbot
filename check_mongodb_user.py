"""Script to check existing MongoDB user data."""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

async def check_user():
    """Check user data in MongoDB."""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    
    # Find the user
    user = await db.user.find_one({"email": "pandeyamartya5151@gmail.com"})
    
    if user:
        print("User found in MongoDB:")
        print(f"Email: {user.get('email')}")
        print(f"Password field: {user.get('password', 'NOT SET')}")
        print(f"Hashed password field: {user.get('hashed_password', 'NOT SET')}")
        print(f"Username: {user.get('username', 'NOT SET')}")
        print(f"Full name: {user.get('full_name', 'NOT SET')}")
        print(f"\nAll fields in document: {list(user.keys())}")
    else:
        print("User not found!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_user())
