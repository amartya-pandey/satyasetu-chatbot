import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

async def get_subadmins():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    mongodb_url = os.getenv('MONGODB_URL')
    client = AsyncIOMotorClient(mongodb_url)
    db = client["SatyaSetu"]
    
    # Get the institution admin
    admin_user = await db.users.find_one({"email": "wejosi2543@kudimi.com"})
    
    if not admin_user:
        print("Admin user not found!")
        return
    
    org_id = admin_user.get('organization')
    if not org_id:
        print("No organization linked!")
        return
    
    # Convert to ObjectId if string
    if isinstance(org_id, str):
        org_id = ObjectId(org_id)
    
    print("=" * 60)
    print(f"Institution: {admin_user.get('meta', {}).get('institutionName')}")
    print(f"Organization ID: {org_id}")
    print("=" * 60)
    
    # Find all users belonging to this organization
    all_users = await db.users.find({"organization": org_id}).to_list(length=1000)
    
    print(f"\nTotal users in this organization: {len(all_users)}")
    print("\n" + "=" * 60)
    print("USERS BREAKDOWN:")
    print("=" * 60)
    
    # Group by role
    role_counts = {}
    for user in all_users:
        role = user.get('role', 'UNKNOWN')
        if role not in role_counts:
            role_counts[role] = []
        role_counts[role].append(user)
    
    for role, users in role_counts.items():
        print(f"\n{role}: {len(users)} user(s)")
        for user in users:
            print(f"  - {user.get('name')} ({user.get('email')})")
            print(f"    ID: {user.get('_id')}")
            if user.get('meta'):
                print(f"    Meta: {user.get('meta')}")
    
    # Count subadmins specifically
    subadmins = [u for u in all_users if u.get('role') in ['ADMIN', 'SUBADMIN', 'INSTITUTION_ADMIN']]
    print("\n" + "=" * 60)
    print(f"Total Sub-Admins: {len(subadmins)}")
    print("=" * 60)
    
    client.close()

asyncio.run(get_subadmins())
