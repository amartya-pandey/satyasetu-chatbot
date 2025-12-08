import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

async def get_university_admin_info():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    mongodb_url = os.getenv('MONGODB_URL')
    client = AsyncIOMotorClient(mongodb_url)
    db = client["SatyaSetu"]
    
    # Find user
    user = await db.users.find_one({"email": "wejosi2543@kudimi.com"})
    
    if user:
        print("=" * 60)
        print("UNIVERSITY ADMIN USER FOUND!")
        print("=" * 60)
        print(f"ID: {user.get('_id')}")
        print(f"Name: {user.get('name')}")
        print(f"Email: {user.get('email')}")
        print(f"Role: {user.get('role')}")
        print(f"Organization ID: {user.get('organization')}")
        print(f"Password (hashed): {user.get('password', 'N/A')[:50]}...")
        print(f"Created At: {user.get('createdAt')}")
        print(f"Updated At: {user.get('updatedAt')}")
        print(f"Meta: {user.get('meta')}")
        
        # If they have an organization, get institution details
        if user.get('organization'):
            org_id = user.get('organization')
            
            # Try as ObjectId
            try:
                if isinstance(org_id, str):
                    org_id = ObjectId(org_id)
                institution = await db.institutions.find_one({"_id": org_id})
            except:
                institution = await db.institutions.find_one({"_id": org_id})
            
            if institution:
                print("\n" + "=" * 60)
                print("INSTITUTION INFO:")
                print("=" * 60)
                print(f"Name: {institution.get('name')}")
                print(f"ID: {institution.get('_id')}")
                print(f"Email: {institution.get('email')}")
                print(f"Address: {institution.get('address')}")
                print(f"Type: {institution.get('type')}")
                
                # Count certificates issued by this institution
                cert_count = await db.certificates.count_documents({"institutionId": org_id})
                print(f"\nTotal Certificates issued by this institution: {cert_count}")
                
                # Show first 5 certificates
                if cert_count > 0:
                    certs = await db.certificates.find({"institutionId": org_id}).limit(5).to_list(length=5)
                    print(f"\nSample certificates (first 5):")
                    for i, cert in enumerate(certs, 1):
                        print(f"  {i}. {cert.get('certificateId')}: {cert.get('student', {}).get('fullName')} - {cert.get('student', {}).get('course')}")
            else:
                print("\nInstitution not found!")
        else:
            print("\nNo organization linked to this user.")
    else:
        print("USER NOT FOUND!")
    
    client.close()

asyncio.run(get_university_admin_info())
