import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_user():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    mongodb_url = os.getenv('MONGODB_URL')
    client = AsyncIOMotorClient(mongodb_url)
    db = client["SatyaSetu"]
    
    user = await db.users.find_one({"email": "pandeyamartya5151@gmail.com"})
    print(f"User found: {user}")
    
    client.close()

asyncio.run(check_user())
