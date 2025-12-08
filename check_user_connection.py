import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

async def check_connection():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    mongodb_url = os.getenv('MONGODB_URL')
    client = AsyncIOMotorClient(mongodb_url)
    db = client["SatyaSetu"]
    
    # Find the user
    user = await db.users.find_one({"email": "togeni2737@roastic.com"})
    
    if user:
        print("=" * 60)
        print("USER FOUND!")
        print("=" * 60)
        print(f"ID: {user.get('_id')}")
        print(f"Name: {user.get('name')}")
        print(f"Email: {user.get('email')}")
        print(f"Role: {user.get('role')}")
        print(f"Organization: {user.get('organization')}")
        print(f"Created At: {user.get('createdAt')}")
        print(f"Meta: {user.get('meta')}")
        
        # Check all possible fields that might link to institution
        print("\n" + "=" * 60)
        print("ALL USER FIELDS:")
        print("=" * 60)
        for key, value in user.items():
            print(f"{key}: {value}")
        
        # Try to find any connection to ICT Mumbai
        ict_institution = await db.institutions.find_one({"name": {"$regex": "Chemical Technology", "$options": "i"}})
        
        if ict_institution:
            print("\n" + "=" * 60)
            print("ICT MUMBAI INSTITUTION:")
            print("=" * 60)
            print(f"ID: {ict_institution.get('_id')}")
            print(f"Name: {ict_institution.get('name')}")
            
            # Check if user's organization matches
            user_org = user.get('organization')
            if user_org:
                if isinstance(user_org, str):
                    user_org = ObjectId(user_org)
                
                if user_org == ict_institution.get('_id'):
                    print("\n✅ USER IS LINKED TO ICT MUMBAI via 'organization' field!")
                else:
                    print(f"\n❌ User organization {user_org} does NOT match ICT ID {ict_institution.get('_id')}")
            
            # Check certificates
            user_certs = await db.certificates.find({"student.email": "togeni2737@roastic.com"}).to_list(length=10)
            if user_certs:
                print(f"\n📜 User has {len(user_certs)} certificate(s):")
                for cert in user_certs:
                    inst_id = cert.get('institutionId')
                    print(f"  - {cert.get('certificateId')} issued by institution ID: {inst_id}")
                    if inst_id == ict_institution.get('_id'):
                        print("    ✅ This certificate is from ICT MUMBAI!")
    else:
        print("USER NOT FOUND!")
    
    client.close()

asyncio.run(check_user_connection())
