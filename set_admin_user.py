import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

async def set_user_as_admin():
    """Set a user as ADMIN and link to institution."""
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    mongodb_url = os.getenv('MONGODB_URL')
    client = AsyncIOMotorClient(mongodb_url)
    db = client["SatyaSetu"]
    
    # Choose which user to make admin
    email = input("Enter email to make ADMIN: ")
    
    user = await db.users.find_one({"email": email})
    if not user:
        print(f"User with email {email} not found!")
        client.close()
        return
    
    print(f"\nFound user: {user.get('name')} ({email})")
    print(f"Current role: {user.get('role', 'USER')}")
    
    # Get first institution from database
    institutions = await db.institutions.find({}).to_list(length=10)
    
    if not institutions:
        print("\nNo institutions found in database!")
        client.close()
        return
    
    print("\nAvailable institutions:")
    for i, inst in enumerate(institutions, 1):
        print(f"{i}. {inst.get('name')} (ID: {inst['_id']})")
    
    choice = int(input("\nSelect institution number (or 0 to skip): "))
    
    if choice > 0 and choice <= len(institutions):
        institution_id = institutions[choice - 1]['_id']
        
        # Update user
        result = await db.users.update_one(
            {"_id": user['_id']},
            {"$set": {
                "role": "ADMIN",
                "organization": institution_id
            }}
        )
        
        print(f"\n✅ Updated user to ADMIN role")
        print(f"✅ Linked to institution: {institutions[choice - 1].get('name')}")
        print(f"✅ Institution ID: {institution_id}")
        
        # Count certificates from this institution
        cert_count = await db.certificates.count_documents({"institutionId": institution_id})
        print(f"\n📜 This institution has {cert_count} certificates")
    else:
        # Just update role without organization
        result = await db.users.update_one(
            {"_id": user['_id']},
            {"$set": {"role": "ADMIN"}}
        )
        print(f"\n✅ Updated user to ADMIN role (no institution linked)")
    
    client.close()

asyncio.run(set_user_as_admin())
