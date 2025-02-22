from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    mongodb_uri: str = os.getenv("MONGODB_URI")
    db_name: str = os.getenv("DB_NAME")

settings = Settings()

client = AsyncIOMotorClient(settings.mongodb_uri)
database = client[settings.db_name]

def get_db():
    return database