import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

async def find_user_certificate():
    load_dotenv()
    mongodb_url = os.getenv('MONGODB_URL')
    client = AsyncIOMotorClient(mongodb_url)
    db = client["SatyaSetu"]
    
    # Find the certificate by ID from user metadata
    cert = await db.certificates.find_one({"certificateId": "SATYA-2025-CB60C98FB3E0A4C0"})
    
    if cert:
        print("Found certificate!")
        print(f"Certificate ID: {cert['certificateId']}")
        print(f"Student: {cert['student']}")
        print(f"Status: {cert['status']}")
        print(f"Issued At: {cert['issuedAt']}")
        print(f"Course: {cert['student'].get('course', 'N/A')}")
        print(f"CGPA: {cert['student'].get('cgpa', 'N/A')}")
    else:
        print("Certificate not found!")
        
        # Try searching by student name
        user = await db.users.find_one({"email": "pandeyamartya5151@gmail.com"})
        name = user.get('name', '')
        print(f"\nSearching for certificates with student name: {name}")
        
        certs = await db.certificates.find({"student.fullName": {"$regex": name, "$options": "i"}}).to_list(length=10)
        print(f"Found {len(certs)} certificates matching name")
        for c in certs:
            print(f"  - {c['certificateId']}: {c['student']['fullName']}")
    
    client.close()

asyncio.run(find_user_certificate())
