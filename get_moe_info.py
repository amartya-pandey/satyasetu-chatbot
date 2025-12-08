import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def get_moe_info():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    mongodb_url = os.getenv('MONGODB_URL')
    client = AsyncIOMotorClient(mongodb_url)
    db = client["SatyaSetu"]
    
    # Find user
    user = await db.users.find_one({"email": "moe@satyasetu.gov.in"})
    
    if user:
        print("=" * 60)
        print("USER FOUND!")
        print("=" * 60)
        print(f"ID: {user.get('_id')}")
        print(f"Name: {user.get('name')}")
        print(f"Email: {user.get('email')}")
        print(f"Role: {user.get('role')}")
        print(f"Organization: {user.get('organization')}")
        print(f"Password (hashed): {user.get('password', 'N/A')[:50]}...")
        print(f"Created At: {user.get('createdAt')}")
        print(f"Meta: {user.get('meta')}")
        
        # If they have an organization, get institution details
        if user.get('organization'):
            org_id = user.get('organization')
            institution = await db.institutions.find_one({"_id": org_id})
            if institution:
                print("\n" + "=" * 60)
                print("INSTITUTION INFO:")
                print("=" * 60)
                print(f"Name: {institution.get('name')}")
                print(f"ID: {institution.get('_id')}")
                
                # Count certificates issued by this institution
                cert_count = await db.certificates.count_documents({"institutionId": org_id})
                print(f"\nCertificates issued by this institution: {cert_count}")
                
                # Show first 3 certificates
                certs = await db.certificates.find({"institutionId": org_id}).limit(3).to_list(length=3)
                print(f"\nSample certificates:")
                for cert in certs:
                    print(f"  - {cert.get('certificateId')}: {cert.get('student', {}).get('fullName')}")
    else:
        print("USER NOT FOUND!")
    
    client.close()

asyncio.run(get_moe_info())
