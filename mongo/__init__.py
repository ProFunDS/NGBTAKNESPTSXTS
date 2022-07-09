from config.tokens import MONGO_PASSWORD

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticCollection

db = AsyncIOMotorClient(
    f"{MONGO_PASSWORD}+address"
    ).MyDB

users: AgnosticCollection = db.users            # users collection
tg_keys: AgnosticCollection = db.telegram_keys  # telegram keys collection
