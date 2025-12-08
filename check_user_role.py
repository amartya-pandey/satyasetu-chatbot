import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_user_role():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    mongodb_url = os.getenv('MONGODB_URL')
    client = AsyncIOMotorClient(mongodb_url)
    db = client["SatyaSetu"]
    
    # Check the logged-in user
    user = await db.users.find_one({"email": "pandeyamartya5151@gmail.com"})
    print(f"User: {user.get('name')}")
    print(f"Email: {user.get('email')}")
    print(f"Role: {user.get('role')}")
    print(f"Organization: {user.get('organization')}")
    
    # Count total certificates in database
    total_certs = await db.certificates.count_documents({})
    print(f"\nTotal certificates in system: {total_certs}")
    
    # Check if user has institution mapping
    if user.get('organization'):
        org_id = user.get('organization')
        institution = await db.institutions.find_one({"_id": org_id})
        if institution:
            print(f"\nInstitution: {institution.get('name')}")
            # Count certificates issued by this institution
            inst_certs = await db.certificates.count_documents({"institutionId": org_id})
            print(f"Certificates issued by this institution: {inst_certs}")
    
    client.close()

asyncio.run(check_user_role())
