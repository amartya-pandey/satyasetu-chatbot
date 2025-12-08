import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

async def check_user_linkage():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    mongodb_url = os.getenv('MONGODB_URL')
    client = AsyncIOMotorClient(mongodb_url)
    db = client["SatyaSetu"]
    
    # Sample a few users to see how organization is stored
    users = await db.users.find({}).limit(10).to_list(length=10)
    
    print("Sample of user records to check organization field:")
    print("=" * 60)
    for user in users:
        print(f"\nEmail: {user.get('email')}")
        print(f"Role: {user.get('role')}")
        print(f"Organization field: {user.get('organization')}")
        print(f"Organization type: {type(user.get('organization'))}")
    
    # Check if there are any users at all in the system
    total_users = await db.users.count_documents({})
    print(f"\n\nTotal users in database: {total_users}")
    
    # Check users with organization field
    users_with_org = await db.users.count_documents({"organization": {"$ne": None}})
    print(f"Users with organization field: {users_with_org}")
    
    client.close()

asyncio.run(check_user_linkage())
