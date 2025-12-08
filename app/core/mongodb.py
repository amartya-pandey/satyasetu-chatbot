from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# MongoDB client
mongodb_client: AsyncIOMotorClient = None


async def connect_to_mongodb():
    """Connect to MongoDB."""
    global mongodb_client
    try:
        mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
        # Test connection
        await mongodb_client.admin.command('ping')
        logger.info(f"Connected to MongoDB at {settings.MONGODB_URL}")
        
        # Initialize Beanie with document models
        from app.models.mongo_models import User, Conversation, Message, Certificate, StudentData
        await init_beanie(
            database=mongodb_client[settings.MONGODB_DB_NAME],
            document_models=[User, Conversation, Message, Certificate, StudentData]
        )
        logger.info("Beanie initialized successfully with all models")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongodb_connection():
    """Close MongoDB connection."""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        logger.info("Closed MongoDB connection")


def get_database():
    """Get MongoDB database instance."""
    return mongodb_client[settings.MONGODB_DB_NAME]
