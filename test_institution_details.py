import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

async def test_institution_details():
    """Test the institution details endpoint logic"""
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    mongodb_url = os.getenv('MONGODB_URL')
    client = AsyncIOMotorClient(mongodb_url)
    db = client["SatyaSetu"]
    
    # Find the Mumbai University SE ID user
    user_email = "wejosi2543@kudimi.com"
    user = await db.users.find_one({"email": user_email})
    
    if not user:
        print(f"User {user_email} not found!")
        return
    
    print("=" * 80)
    print(f"USER: {user.get('name')} ({user.get('email')})")
    print(f"Role: {user.get('role')}")
    print("=" * 80)
    
    org_id = user.get('organization')
    if not org_id:
        print("No organization linked!")
        return
    
    # Convert to ObjectId if string
    if isinstance(org_id, str):
        org_id = ObjectId(org_id)
    
    # Get institution details
    institution = await db.institutions.find_one({"_id": org_id})
    if institution:
        print("\nINSTITUTION DETAILS:")
        print(f"  Name: {institution.get('name')}")
        print(f"  ID: {institution.get('_id')}")
        print(f"  Email: {institution.get('email')}")
        print(f"  Type: {institution.get('type')}")
    
    # Get all sub-admins linked to this institution
    all_users = await db.users.find({"organization": org_id}).to_list(length=1000)
    
    sub_admins = [u for u in all_users if u.get('role') in ['ADMIN', 'SUBADMIN', 'INSTITUTION_ADMIN', 'INSTITUTION']]
    regular_users = [u for u in all_users if u.get('role') not in ['ADMIN', 'SUBADMIN', 'INSTITUTION_ADMIN', 'INSTITUTION']]
    
    print("\n" + "=" * 80)
    print(f"SUB-ADMINS ({len(sub_admins)}):")
    print("=" * 80)
    for admin in sub_admins:
        print(f"  • {admin.get('name')} ({admin.get('email')})")
        print(f"    Role: {admin.get('role')}")
        print(f"    ID: {admin.get('_id')}")
        if admin.get('meta'):
            print(f"    Meta: {admin.get('meta')}")
        print()
    
    print("=" * 80)
    print(f"REGULAR USERS ({len(regular_users)}):")
    print("=" * 80)
    for u in regular_users[:5]:  # Show first 5
        print(f"  • {u.get('name')} ({u.get('email')}) - Role: {u.get('role')}")
    if len(regular_users) > 5:
        print(f"  ... and {len(regular_users) - 5} more users")
    
    # Get certificates issued by this institution
    total_certs = await db.certificates.count_documents({"institutionId": org_id})
    print("\n" + "=" * 80)
    print(f"CERTIFICATES ISSUED: {total_certs}")
    print("=" * 80)
    
    if total_certs > 0:
        # Get first 10 certificates with issuer details
        certs = await db.certificates.find({"institutionId": org_id}).limit(10).to_list(length=10)
        
        print("\nSample Certificates (first 10):")
        for i, cert in enumerate(certs, 1):
            print(f"\n{i}. {cert.get('certificateId')}")
            print(f"   Student: {cert.get('student', {}).get('fullName')}")
            print(f"   Course: {cert.get('student', {}).get('course')} - {cert.get('student', {}).get('department')}")
            print(f"   Roll: {cert.get('student', {}).get('rollNumber')}")
            print(f"   CGPA: {cert.get('student', {}).get('cgpa')}")
            print(f"   Status: {cert.get('status')}")
            print(f"   Blockchain: {cert.get('blockchainStatus')}")
            
            # Get issuer details
            issuer_id = cert.get('issuerId')
            if issuer_id:
                issuer = await db.users.find_one({"_id": issuer_id})
                if issuer:
                    print(f"   Issued By: {issuer.get('name')} ({issuer.get('email')}) - Role: {issuer.get('role')}")
            
            print(f"   PDF: {cert.get('pdfUrl')}")
    
    print("\n" + "=" * 80)
    print("SUMMARY:")
    print("=" * 80)
    print(f"Institution: {institution.get('name') if institution else 'N/A'}")
    print(f"Total Sub-Admins: {len(sub_admins)}")
    print(f"Total Regular Users: {len(regular_users)}")
    print(f"Total Certificates: {total_certs}")
    print("=" * 80)
    
    client.close()

asyncio.run(test_institution_details())
