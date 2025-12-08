import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_collections():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    mongodb_url = os.getenv('MONGODB_URL')
    client = AsyncIOMotorClient(mongodb_url)
    db = client["SatyaSetu"]
    
    # List all collections
    collections = await db.list_collection_names()
    print(f"Collections in SatyaSetu database: {collections}")
    
    # Check user
    user = await db.users.find_one({"email": "pandeyamartya5151@gmail.com"})
    print(f"\nUser ID: {user['_id']}")
    
    # Check if certificates collection exists
    if 'certificates' in collections:
        cert_count = await db.certificates.count_documents({})
        print(f"\nTotal certificates in collection: {cert_count}")
        
        # Try to find certificates by user email
        certs_by_email = await db.certificates.find({"email": "pandeyamartya5151@gmail.com"}).to_list(length=100)
        print(f"Certificates by email: {len(certs_by_email)}")
        if certs_by_email:
            print("Sample certificate:", certs_by_email[0])
        
        # Try to find by user_id
        certs_by_id = await db.certificates.find({"user_id": str(user['_id'])}).to_list(length=100)
        print(f"Certificates by user_id: {len(certs_by_id)}")
        
        # Show all certificate fields
        sample = await db.certificates.find_one({})
        if sample:
            print(f"\nSample certificate structure: {sample.keys()}")
            print(f"Full certificate: {sample}")
    
    client.close()

asyncio.run(check_collections())
