import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

async def check_cert_structure():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    mongodb_url = os.getenv('MONGODB_URL')
    client = AsyncIOMotorClient(mongodb_url)
    db = client["SatyaSetu"]
    
    # Get a sample certificate
    cert = await db.certificates.find_one()
    
    if cert:
        print("Sample Certificate Structure:")
        print("=" * 60)
        for key, value in cert.items():
            print(f"{key}: {value}")
    else:
        print("No certificates found in database")
    
    client.close()

asyncio.run(check_cert_structure())
